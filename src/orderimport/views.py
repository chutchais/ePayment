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

from .forms import CreateOrderForm

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    paginate_by = 50
    def get_queryset(self):
        query = self.request.GET.get('q')
        # lacking_stock = self.request.GET.get('lacking')
        # over_stock = self.request.GET.get('over')
        print('Verify payment :',self.request.user.has_perm('order.verify_payment'))
        if query :
            return Order.objects.filter(Q(name__icontains=query) |
                                    Q(booking__name__icontains=query) ,
                                    user__username=self.request.user ).select_related('bl').order_by('-updated')

        if self.request.user.has_perm('orderimport.verify_payment') or  self.request.user.has_perm('orderimport.update_payment') :
            return Order.objects.all().select_related('bl').order_by('-updated')

        return Order.objects.filter(user__username=self.request.user).select_related('bl').order_by('-updated')
    
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
            ref =   datetime.datetime.now(tz=tz).strftime("%M%S")
            ref =   f'E{ref}'

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

class OrderUpdateSlip(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['payment_slip']
    template_name_suffix = '_update_payslip_form'

# Added on Oct 28,2020 -- To support WHT slip upload
class OrderUpdateWHT(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['wht_slip']
    template_name_suffix = '_update_whtslip_form'
