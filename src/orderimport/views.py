from django.shortcuts import render
import urllib3
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.views.generic.base import TemplateView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count,Sum

from bl.models import BillofLadding
from .models import Order,Container
from user_profile.models import Address
from tax.models import Tax
import json

from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import CreateOrderForm

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    paginate_by = 50
    def get_queryset(self):
        query = self.request.GET.get('q')
        # lacking_stock = self.request.GET.get('lacking')
        # over_stock = self.request.GET.get('over')
        # print('Verify payment :',self.request.user.has_perm('order.verify_payment'))
        # if query :
        #     return Order.objects.filter(Q(name__icontains=query) |
        #                             Q(bl__name__icontains=query) ,
        #                             user__username=self.request.user ).select_related('bl').order_by('-updated')

        # if self.request.user.has_perm('orderimport.verify_payment') or  self.request.user.has_perm('orderimport.update_payment') :
        #     return Order.objects.all().select_related('bl').order_by('-updated')

        # return Order.objects.filter(user__username=self.request.user).select_related('bl').order_by('-updated')
    
        if query :
            if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
                # For Staff or Admin
                # Modify on Nov 20,2020 -- To support search by User name
                return Order.objects.filter(Q(name__icontains=query) |
                                        Q(bl__name__icontains=query)|
                                        Q(user__username=query)).select_related('bl').order_by('-updated')
                                        #Q(booking__name__icontains=query)| -->Removed for optimize
            else:
                return Order.objects.filter(Q(name__icontains=query) |
                                        Q(bl__name__icontains=query) ,
                                        user__username=self.request.user ).select_related('bl').order_by('-updated')
                                        # Q(booking__name__icontains=query) ,-->Removed for optimize
        if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
            return Order.objects.all().select_related('bl').order_by('-updated')[:300]

        return Order.objects.filter(user__username=self.request.user).select_related('bl').order_by('-updated')[:300]
    
    
    def get_context_data(self,**kwargs):
        context = super(OrderListView,self).get_context_data(**kwargs)
        # context['addresses'] = Address.objects.filter(user__username=self.request.user)
        return context

class OrderDetailView(LoginRequiredMixin,DetailView):
    # model = Order
    queryset = Order.objects.select_related('bl','address')
    def get_context_data(self,**kwargs):
        context = super(OrderDetailView,self).get_context_data(**kwargs)
        # context['qr_url'] = settings.QR_CODE_ENDPOINT_URL#'http://10.24.50.91:8010/billing/'#
        context['qr_url'] = reverse_lazy('order:list')
        context['slip_verify_url'] = settings.SLIP_VERIFY_ENDPOINT_URL
        # For Container summary , SizeXCount(*) -- Total Price
        order = super().get_object()
        summary = order.containers.values('cont_size').annotate(
                count=Count('container'),
                total_ex_vat= Sum('total') 
                                # + ((Sum('total')*order.vat_rate)/100) 
                                # - ((Sum('total')*order.wht_rate)/100) if order.wht else 0
                )
        context['summary'] = summary
        # for c in obj.containers.all():
        #     print(c)
        return context
    
        # Added on Nov 25,2020 -- To protect access by other
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)

        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)


def post_container(request):
    import json
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateOrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            bl              = form.cleaned_data['bl']
            wht             = form.cleaned_data['wht']
            charge          = form.cleaned_data['charge']
            vat_rate        = form.cleaned_data['vat_rate']
            wht_rate        = form.cleaned_data['wht_rate']
            grand_total     = form.cleaned_data['grand_total']
            containers_json = form.cleaned_data['containers']
            address         = form.cleaned_data['address']
            containers      = json.loads(containers_json)
            # Added on Oct 8,2020 
            seperate_bill   = form.cleaned_data['seperatebill']
            # ----------------------------
            paid_until      = form.cleaned_data['paid_until']
            rent            = form.cleaned_data['rent']

            # Create Order
            # ref = datetime.now().strftime("%H%M%S")
            # Modify on Oct 22,2020 -- To Change Ref1 to E%M%S format 
            # ref =   datetime.now().strftime("%M%S")
            # Modify on Oct 29,2020 -- To support Timezone
            import datetime, pytz
            tz = pytz.timezone('Asia/Bangkok')
            ref =   datetime.datetime.now(tz=tz).strftime("%H%M%S")
            ref =   f'I{ref}'

            # Mofigy on Aug 17,2020
            # To limit Order name to be 15 digits (last 15 digits) , without DLCB or DLCM
            order_name = f'{bl}{ref}'[-15:]

            user        = User.objects.get(username=request.user)
            bl_obj      = BillofLadding.objects.get(name=bl,user=user)
            address_obj = Address.objects.get(pk=address)
            
            # print(booking,ref,order_name,booking_obj,user)
            if len(containers) > 0:
            #     booking_obj = Booking.objects.get(name=booking)
                order = Order(name=order_name,ref=ref,
                        bl=bl_obj,
                        address=address_obj,
                        charge=charge,grand_total=grand_total,
                        vat_rate = vat_rate, wht_rate=wht_rate,
                        container_count=len(containers),
                        wht=wht,user=user,seperate_bill=seperate_bill,
                        paid_until=paid_until,rent=rent)
                order.save()
                # save containers
                container_count =0
                for container in containers:
                    # print(container['container'])
                    # Added on Oct 30,2020 -- To skip if total=0
                    if container['total'] > 0:
                        print(container)
                        c = Container(order=order,container=container['container'],
                            cont_size=int(container['discharge']['size'].replace('.00','')),
                            iso=container['discharge']['iso'],
                            lifton=container['lolo'],
                            relocation=container['relo'],
                            storage=container['rate1']+container['rate2']+container['rate3'],
                            total =container['total'],
                            user=user)
                        c.save()
                        container_count = container_count+1

                # Update Booking Terminal
                # Added on July 22,2020 by Chutchai
                terminal = container['discharge']['terminal']
                if not bl_obj.terminal :
                    bl_obj.terminal = terminal
                    bl_obj.save()
                
                # Added on Aug 17,2020 -- to update QRid to Order
                terminal_prefix = 'LCB' if terminal=='LCB1' else 'LCM'
                order.qrid = f'D{terminal_prefix}{order_name}'
                # Added on Oct 30,2020 -- To refresh Container count
                order.container_count =  container_count
                order.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse_lazy('orderimport:detail',kwargs={'pk': order.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateOrderForm()

    return render(request, 'orderimport/orderimport_form.html', {'form': form})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orderimport:list')

        # Added on Nov 25,2020 -- To protect access by other
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)

        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)


class OrderUpdateDo(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['do']
    template_name_suffix = '_update_do_form'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)

        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class OrderUpdateSlip(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['payment_slip']
    template_name_suffix = '_update_payslip_form'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)

        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

# Added on Oct 28,2020 -- To support WHT slip upload
class OrderUpdateWHT(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['wht_slip']
    template_name_suffix = '_update_whtslip_form'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)

        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)


class OrderUpdateExecuteJob(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['execute_job']
    template_name_suffix = '_update_executejob_form'

    def form_valid(self, form):
        import datetime, pytz
        tz = pytz.timezone('Asia/Bangkok')
        form.instance.execute_date = datetime.datetime.now(tz=tz)#datetime.now()
        # Added on Oct 29,2020 -- To save executor
        form.instance.execute_by = self.request.user
         # Added on Dec 3,2020 -- To Update Invoice number.
        if form.instance.execute_job :
            from .tasks import update_invoice_by_order
            update_invoice_by_order(form.instance)
            # async_task('order.tasks.update_invoice_by_order',form.instance)
        # ----------------------------------------------
        return super(OrderUpdateExecuteJob, self).form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)

        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class OrderUpdatePaid(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['paid','payment_ref']
    template_name_suffix = '_update_paid_form'

    def form_valid(self, form):
        form.instance.payment_inspector = self.request.user
        import datetime, pytz
        tz = pytz.timezone('Asia/Bangkok')
        form.instance.payment_date = datetime.datetime.now(tz=tz)#datetime.now()
        return super(OrderUpdatePaid, self).form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)
        else :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)
