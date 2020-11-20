from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import redirect
# Create your views here.
import urllib3
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count,Sum
from user_profile.models import Address
from order.models import Order,Container
from order.forms import OrderPaySlipForm,CreateOrderForm,OrderPaymentForm
from oog.models import Oog
from booking.models import Booking
from django.http import Http404

@login_required
def index(request):
    context = {
        'addresses' : Address.objects.filter(user__username=request.user),
        'orders' : Order.objects.filter(user__username=request.user)
    }
    return render(request, 'home.html',context)

def post_container(request):
    import json
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateOrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                # process the data in form.cleaned_data as required
                booking = form.cleaned_data['booking']
                wht = form.cleaned_data['wht']
                charge = form.cleaned_data['charge']
                vat_rate = form.cleaned_data['vat_rate']
                wht_rate = form.cleaned_data['wht_rate']
                grand_total = form.cleaned_data['grand_total']
                containers_json = form.cleaned_data['containers']
                address = form.cleaned_data['address']
                containers = json.loads(containers_json)
                # Added on Oct 8,2020 
                seperate_bill = form.cleaned_data['seperatebill']
                # ----------------------------

                # Create Order
                # ref = datetime.now().strftime("%H%M%S")
                # Modify on Oct 22,2020 -- To Change Ref1 to E%M%S format 
                # ref =   datetime.now().strftime("%M%S")
                # Modify on Oct 29,2020 -- To support Timezone
                import datetime, pytz
                tz = pytz.timezone('Asia/Bangkok')
                # ref =   datetime.datetime.now(tz=tz).strftime("%H%M")
                # Modify on Nov 11,2020 -- To change ref to E%H%M%S format (7 digits)
                ref =   datetime.datetime.now(tz=tz).strftime("%H%M%S")
                ref =   f'E{ref}'

                # Mofigy on Aug 17,2020
                # To limit Order name to be 15 digits (last 15 digits) , without DLCB or DLCM
                order_name = f'{booking}{ref}'[-15:]

                user = User.objects.get(username=request.user)
                booking_obj = Booking.objects.get(name=booking,user=user)
                address_obj = Address.objects.get(pk=address)
                
                # print(booking,ref,order_name,booking_obj,user)
                if len(containers) > 0:

                    order = Order(name=order_name,ref=ref,
                            booking=booking_obj,
                            address=address_obj,
                            charge=charge,grand_total=grand_total,
                            vat_rate = vat_rate, wht_rate=wht_rate,
                            container_count=len(containers),
                            wht=wht,user=user,seperate_bill=seperate_bill)
                    order.save()
                    # save containers
                    container_count =0
                    for container in containers:
                        # print(container['container'])
                        # Added on Oct 30,2020 -- To skip if total=0
                        if container['tariff_sum_total'] > 0:
                            c = Container(order=order,container=container['container'],
                                cont_size=container['size'],
                                iso=container['iso'],
                                is_oog=True if container['iso']=='yes' else False,
                                tariff=container['tariff'],
                                total =container['tariff_sum_total'],
                                user=user)
                            c.save()
                            container_count = container_count+1

                    # Update Booking Terminal
                    # Added on July 22,2020 by Chutchai
                    terminal = container['terminal']
                    if not booking_obj.terminal :
                        booking_obj.terminal = terminal
                        booking_obj.save()
                    
                    # Added on Aug 17,2020 -- to update QRid to Order
                    terminal_prefix = 'LCB' if terminal=='LCB1' else 'LCM'
                    order.qrid = f'D{terminal_prefix}{order_name}'
                    # Added on Oct 30,2020 -- To refresh Container count
                    order.container_count =  container_count
                    order.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse_lazy('order:detail',kwargs={'pk': order.id}))
            except IntegrityError as e:
                return render(request,'order/error.html', {'message': e.__cause__})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateOrderForm()

    return render(request, 'order/order_form.html', {'form': form})


def update_payment(request):
    import json
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OrderPaymentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            order_id        = form.cleaned_data['id']
            payment_date    = form.cleaned_data['payment_date']
            payment_ref     = form.cleaned_data['payment_date']
            # Create Order
            user = User.objects.get(username=request.user)
            order = Order.objects.get(name=order_id,user=user)
            
            # print(booking,ref,order_name,booking_obj,user)
            order.paid          = True
            order.payment_date  = ''
            order.payment_ref   = ''
            order.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse_lazy('order:detail',kwargs={'pk': order.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateOrderForm()

    return render(request, 'order/order_form.html', {'form': form})

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    paginate_by = 50
    def get_queryset(self):
        query = self.request.GET.get('q')
        # lacking_stock = self.request.GET.get('lacking')
        # over_stock = self.request.GET.get('over')
        # print('Verify payment :',self.request.user.has_perm('order.verify_payment'))
        if query :
            if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
                # For Staff or Admin
                # Modify on Nov 20,2020 -- To support search by User name
                return Order.objects.filter(Q(name__icontains=query) |
                                        Q(user__username=query)).select_related('booking').order_by('-updated')
                                        #Q(booking__name__icontains=query)| -->Removed for optimize
            else:
                return Order.objects.filter(Q(name__icontains=query) ,
                                        user__username=self.request.user ).select_related('booking').order_by('-updated')
                                        # Q(booking__name__icontains=query) ,-->Removed for optimize
        if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
            return Order.objects.all().select_related('booking').order_by('-updated')[:200]

        return Order.objects.filter(user__username=self.request.user).select_related('booking').order_by('-updated')[:200]
    
    def get_context_data(self,**kwargs):
        context = super(OrderListView,self).get_context_data(**kwargs)
        # context['addresses'] = Address.objects.filter(user__username=self.request.user)
        return context


class OrderCreateView(LoginRequiredMixin,CreateView):
    model = Order
    fields = ['booking','name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ref = datetime.now().strftime("%H%M%S")
        return super(OrderCreateView, self).form_valid(form)

class OrderDetailView(LoginRequiredMixin,DetailView):
    # model = Order
    queryset = Order.objects.select_related('booking','address')
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

class OrderUpdateSlip(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['payment_slip']
    template_name_suffix = '_update_payslip_form'

# Added on Oct 28,2020 -- To support WHT slip upload
class OrderUpdateWHT(LoginRequiredMixin,UpdateView):
    model = Order
    fields = ['wht_slip']
    template_name_suffix = '_update_whtslip_form'

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
        return super(OrderUpdateExecuteJob, self).form_valid(form)

class OrderDeleteView(LoginRequiredMixin,DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.user == request.user) or request.user.is_superuser or request.user.is_staff :
            self.object.delete()
            return redirect(self.get_success_url())
        else:
            raise Http404("Not allow to delete") #or return HttpResponse('404_url')




# Container Detail
class ContainerListView(LoginRequiredMixin,ListView):
    model = Container
    paginate_by = 100

    def get_queryset(self):
        query = self.request.GET.get('q')
        # lacking_stock = self.request.GET.get('lacking')
        # over_stock = self.request.GET.get('over')
        if query :
            return Container.objects.filter(Q(container__icontains=query) |
                                    Q(order__name__icontains=query) ,
                                    user__username=self.request.user ).select_related('order','user').order_by('-updated')

        # if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
        #     return Container.objects.all().order_by('-updated')

        return Container.objects.filter(user__username=self.request.user).select_related('order','user').order_by('-updated')

class ContainerDetailView(LoginRequiredMixin,DetailView):
    # model = Container
    queryset = Container.objects.select_related('order')
    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     # lacking_stock = self.request.GET.get('lacking')
    #     # over_stock = self.request.GET.get('over')
    #     print('Verify payment :',self.request.user.has_perm('order.verify_payment'))
    #     if query :
    #         return Order.objects.filter(Q(name__icontains=query) |
    #                                 Q(booking__name__icontains=query) ,
    #                                 user__username=self.request.user ).order_by('-updated')

    #     if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
    #         return Order.objects.all().order_by('-updated')

    #     return Order.objects.filter(user__username=self.request.user).order_by('-updated')
    
    # def get_context_data(self,**kwargs):
    #     context = super(OrderListView,self).get_context_data(**kwargs)
    #     # context['addresses'] = Address.objects.filter(user__username=self.request.user)
    #     return context


# @login_required
# def add_payslip(request,order):
#   print(order)
#     upload = OrderPaySlipForm()
#     if request.method == 'POST':
#         upload = AddressForm(request.POST, request.FILES)
#         if upload.is_valid():
#             # order = Order.objects.get(name='')
#             # user = User.objects.get(username=request.user)
#             # # print ('Current user',user)
#             # # profile.user = user
            
#             # order.save()
#             return redirect('profile_setting')
#         else:
#             return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
#     else:
#         return render(request, 'profile/address.html', {'address_form':upload})

# def index(request):

#   cart_product_form = CartAddProductForm()
#   context = {
#   'container': '556677800',
#   'cart_product_form': cart_product_form
#   }
#   return render(request, 'order/index.html',context)

# def create_order(request):
#   booking = request.POST.get('booking')
#   object_list = None
#   # print('Start Booking- %s' % booking)
    
#   # del request.session[settings.CART_SESSION_ID]
#   cart = request.session.get(settings.CART_SESSION_ID)
#   if booking :

#       # cart = request.session.get(settings.CART_SESSION_ID)
#       cart.clear()

#       cart = Cart(request)


#       object_list = get_booking_detail(booking)
#       for item in  object_list:
#           # print (item['size'])
#           cart.add(container=item['container'],category='E',size=item['size'],
#                 full=True if item['full'] == 'F' else False ,
#                 oog=False, con_type=item['container_type'],
#                 status=item['status'])


#   context = {
#       'booking' : booking,
#       'object_list': object_list,
#       'cart': cart
#   }
#   return render(request, 'order/create_order.html',context)

# def clear_cart(request):
#   self.cart.clear()


# def get_booking_detail(booking):
#   import json
#   http = urllib3.PoolManager()
#   r = http.request('GET', f'http://192.168.10.16:5001/booking/{booking}')
#   return json.loads(r.data.decode('utf-8'))


# Get Booking Information from CMOS
import json
from django.http import JsonResponse
from tariff.views import get_tariff_detail

def get_tarriff(full='F',size='20',oog='no'):
    # http = urllib3.PoolManager()
    # url = f"http://127.0.0.1:8000/tariff/?category=E&full={full}&size={size}&oog={oog}"
    # r = http.request('GET', url)
    # print(r.data)
    # return json.loads(r.data.decode('utf-8'))
    full_boolean        = True if full=='F' else False
    oog_boolean         = True if oog=='yes' else False
    size= size.replace('.00','')
    return get_tariff_detail(category='E',full=full_boolean,size=size,oog=oog_boolean)

def init_db():
    # CTCS
    import pyodbc
    cnxn = pyodbc.connect('DRIVER={iSeries Access ODBC Driver};QRYSTGLMT=-1;PKG=QGPL/DEFAULT(IBM),2,0,1,0,512;'\
                            'LANGUAGEID=ENU;DFTPKGLIB=QGPL;DBQ=QGPL;'\
                            'SYSTEM=192.168.0.6;UID=OPSCC;PWD=OPSCC21')
    # cnxn = pyodbc.connect('DRIVER={IBM DB2 ODBC DRIVER};'\
    #                         'LANGUAGEID=ENU;DFTPKGLIB=QGPL;DBQ=QGPL;'\
    #                         'SYSTEM=192.168.0.6;UID=OPSCC;PWD=OPSCC21')
    cursor = cnxn.cursor()
    return cursor

def db_ctcs_get_pod(hdid10,cursor_ctcs):
    import decimal
    cursor_ctcs.execute("select BZID10,"\
                        "VUPL02 as country,"\
                        "VUPP02 as port,"\
                        "VUPO02 as port_name "\
                        "FROM LCB1NET.CTLTHD02 WHERE HDID10=" + hdid10 )
    row = cursor_ctcs.fetchone()
    columns = [column[0].lower() for column in cursor_ctcs.description]
    clean_d = { k:v.strip() for k, v in zip(columns,row) if isinstance(v, str)}
    clean_date = { k:v for k, v in zip(columns,row) if isinstance(v, decimal.Decimal)}
    clean_d.update(clean_date)
    # print(dict(clean_d), file=sys.stdout)
    if row != None:
        return dict(clean_d)
    return ''

def db_ctcs_get_gatein(bzid01,cursor_ctcs):
    from datetime import datetime
    import decimal
    cursor_ctcs.execute("select VMSR01 as by,VMYK01,VMID01 as license_plate,"\
                        "ATAD01 as date_in,ATAT01 as time_in,VMSN01 as company "\
                        "from LCB1NET.CTVSIT02 where BZID01=" + bzid01 )
    row = cursor_ctcs.fetchone()

    if row == None:
        return {}
    

    columns = [column[0].lower() for column in cursor_ctcs.description]
    clean_d = { k:v.strip() for k, v in zip(columns,row) if isinstance(v, str)}
    clean_date = { k:v for k, v in zip(columns,row) if isinstance(v, decimal.Decimal)}
    clean_d.update(clean_date)
    
    date_in_str = str(clean_d.get("date_in", None))
    time_in_str = str(clean_d.get("time_in", None))
    date_in_date = datetime(int(date_in_str[:4]),int(date_in_str[4:6]),int(date_in_str[-2:]))
    if len(time_in_str) == 6 :
        hour_in = int(time_in_str[:2])
        minute_in = int(time_in_str[2:4])
        second_in = int(time_in_str[-2:])
    if len(time_in_str) == 5 :
        hour_in = int(time_in_str[:1])
        minute_in = int(time_in_str[1:3])
        second_in = int(time_in_str[-2:])
    if len(time_in_str) == 4 :
        hour_in = 0
        minute_in = int(time_in_str[:2])
        second_in = int(time_in_str[-2:])
    date_in_date=date_in_date.replace(hour=hour_in,minute=minute_in,second=second_in)
    clean_d.update({'datetime_in' :date_in_date })
    del clean_d['time_in']
    del clean_d['date_in']
    return dict(clean_d)

def db_ctcs_get_load(hdid10,cursor_ctcs):
    from datetime import datetime
    import decimal
    # cursor_ctcs.execute("select HDDT03 as date_out,HDTD03 as time_out "\
    #                   "FROM LCB1NET.CTHNDL01 WHERE HDID03 =" + hdid10 )
    # row = cursor_ctcs.fetchone()
    # print(hdid10, file=sys.stdout)

    cursor_ctcs.execute("select HDDT03 as date_out,HDTD03 as time_out, "\
                        "VMID01 as vessel_code,MVVA47 as vessel_name,RSUT01 as voy,TOPR01 as terminal "\
                        "from LCB1DAT.loaded "\
                        "where HDRA03 =" + hdid10)
    row = cursor_ctcs.fetchone()
    # print('PASS', file=sys.stdout)

    if row == None:
        return {}

    columns = [column[0].lower() for column in cursor_ctcs.description]
    clean_d = { k:v.strip() for k, v in zip(columns,row) if isinstance(v, str)}
    clean_date = { k:v for k, v in zip(columns,row) if isinstance(v, decimal.Decimal)}
    clean_d.update(clean_date)
    
    date_in_str = str(clean_d.get("date_out", None))
    time_in_str = str(clean_d.get("time_out", None))
    date_in_date = datetime(int(date_in_str[:4]),int(date_in_str[4:6]),int(date_in_str[-2:]))

    if len(time_in_str) == 6 :
        hour_in = int(time_in_str[:2])
        minute_in = int(time_in_str[2:4])
        second_in = int(time_in_str[-2:])
    if len(time_in_str) == 5 :
        hour_in = int(time_in_str[:1])
        minute_in = int(time_in_str[1:3])
        second_in = int(time_in_str[-2:])
    if len(time_in_str) == 4 :
        hour_in = 0
        minute_in = int(time_in_str[:2])
        second_in = int(time_in_str[-2:])
    if len(time_in_str) == 3 :
        hour_in = 0
        minute_in = int(time_in_str[:1])
        second_in = int(time_in_str[-2:])
    if len(time_in_str) == 2 :
        hour_in = 0
        minute_in = 0
        second_in = int(time_in_str[-2:])
    date_in_date = date_in_date.replace(hour=hour_in,minute=minute_in,second=second_in)
    clean_d.update({'datetime_out' :date_in_date })
    del clean_d['time_out']
    del clean_d['date_out']
    return dict(clean_d)

def db_ctcs_exp_get_booking(booking):
    from datetime import datetime
    import decimal
    cursor_ctcs = init_db()
    cursor_ctcs.execute("select LTID02,HDID10,BTWI03 as cash,"\
                        "CNBT03 as full,"\
                        "CNHH03 as high,"\
                        "CNID10 as container,"\
                        "CNIS03 as iso,"\
                        "CNLL03 as size,"\
                        "CNTP03 as container_type,"\
                        "HDDT03,"\
                        "LTFS02 as status,"\
                        "LTSQ02,"\
                        "LTSR02 as direction,"\
                        "LYND05 as line,"\
                        "ORCD05 as date_in,"\
                        "ORCT05 as time_in,"\
                        "ORFS05 as status2,"\
                        "ORID05,"\
                        "OROP05 as comment,"\
                        "ORRF05 as booking,"\
                        "ORTP05 as in_by, "\
                        "VUVI02 as vessel_code,"\
                        "VURS02 as voy "\
                    "from lcb1net.ctordr11 "\
                    "where orrf05='" + booking + "' "\
                    "and ortp05 in ('BKG','FOT','MTI','CNA') and ORFS05 <>'CAN' "\
                    "order by CNID10 ")

    rows = cursor_ctcs.fetchall()
    columns = [column[0].lower() for column in cursor_ctcs.description]
    # print(columns, file=sys.stdout)
    if rows:
        
        # print('Found Data ' + hid , file=sys.stdout)
        results = []
        for row in rows:
            hidid = str(row[1])
            pod =  db_ctcs_get_pod(hidid,cursor_ctcs)
            load ={}
            # print(hidid)
            load = db_ctcs_get_load(hidid,cursor_ctcs)
            # print('POD Data ' + str(pod.get('bzid10',None)) , file=sys.stdout)
            truck_in = {}
            if pod.get('bzid10',None) != 0 :
                truck_in = db_ctcs_get_gatein(str(pod.get('bzid10',None)),cursor_ctcs)
            clean_d = { k:v.strip() for k, v in zip(columns,row) if isinstance(v, str)}
            
            clean_date = { k:v for k, v in zip(columns,row) if isinstance(v, decimal.Decimal)}
            clean_d.update(clean_date)

            date_in_str = str(clean_d.get("date_in", None))
            time_in_str = str(clean_d.get("time_in", None))
            date_in_date = datetime(int(date_in_str[:4]),int(date_in_str[4:6]),int(date_in_str[-2:]))
            if len(time_in_str) == 6 :
                hour_in = int(time_in_str[:2])
                minute_in = int(time_in_str[2:4])
                second_in = int(time_in_str[-2:])
            if len(time_in_str) == 5 :
                hour_in = int(time_in_str[:1])
                minute_in = int(time_in_str[1:3])
                second_in = int(time_in_str[-2:])
            if len(time_in_str) == 4 :
                hour_in = 0
                minute_in = int(time_in_str[:2])
                second_in = int(time_in_str[-2:])
            if len(time_in_str) == 3 :
                hour_in = 0
                minute_in = int(time_in_str[:1])
                second_in = int(time_in_str[-2:])
            if len(time_in_str) == 2 :
                hour_in = 0
                minute_in = 0
                second_in = int(time_in_str[-2:])
            date_in_date=date_in_date.replace(hour=hour_in,minute=minute_in,second=second_in)
            clean_d.update({'datetime_in' :date_in_date })
            clean_d.update({'pod' :pod })
            clean_d.update({'in' :truck_in })
            clean_d.update({'load' :load })

            'For tariff'
            sum_price = 0
            size = str(clean_d.get('size', '40'))
            clean_d.update({'size' :size.replace('.00','') })

            # TODO -- check Continer is OOG
            is_oog = False #is_OOG(clean_d.get('container', ''),booking)
            clean_d.update({'oog' :is_oog })
            # -----------------------------

            if str(clean_d.get("status", None)) == 'RGS' and clean_d.get('container', '') != '':

                full = str(clean_d.get('full', 'F'))
                tariff = get_tarriff(full=full,size=size,oog=is_oog)#-----TODO
                size = str(clean_d.get('size', '40'))
                size= size.replace('.00','')
                if len(tariff) > 0 :
                    sum_price = sum(v for k,v in tariff.items())

                clean_d.update({'tariff' :tariff })
            else :
                clean_d.update({'tariff' :{} })

            clean_d.update({'tariff_sum_total' :sum_price })

            results.append(dict(clean_d))

        # print(results, file=sys.stdout)
        return results

# def get_booking_info(request,booking):
#     Objects = db_ctcs_exp_get_booking(booking)
#     response = JsonResponse(Objects, safe=False)
#     response['Access-Control-Allow-Origin'] = '*'
#     response['Access-Control-Allow-Headers'] = '*'
#     return response

def get_booking_info(request,booking):
    import json
    http = urllib3.PoolManager()
    # print ('get_booking_info')
    r = http.request('GET', f'http://192.168.10.16:5001/booking/{booking}')
    # return json.loads(r.data.decode('utf-8'))
    response = JsonResponse(json.loads(r.data.decode('utf-8')), safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = '*'
    return response

# def is_OOG(container,booking):
#     try:
#         oog = Oog.objects.get(booking=booking,container=container)
#         if oog :
#             return 'yes'
#     except Exception as e:
#         return 'no'
#     return 'no'