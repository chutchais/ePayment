from datetime import datetime
from .models import Order

from django.conf import settings
from django_q.tasks import async_task
import requests

# Added on Dec 23,2020 -- To Manual check pay slip
def verify_payment_schedule():
    # 1)Get Order list (Paid= False and payment_slip = None)
    from order.models import Order
    pending_orders = Order.objects.filter(paid=False).exclude(payment_slip__exact='').select_related('booking')
    # 2)Check Payment (To TMB)
    for order in pending_orders:
        async_task('order.services.verify_payment_order',order)
        

    # pass
def verify_payment_order(order):
    check_url       = settings.SLIP_VERIFY_ENDPOINT_URL
    qrid            = order.qrid
    terminal        = order.booking.terminal
    billerid        = '010553811088480' if terminal=='LCB1' else '011554701016180'
    print(f'Verify payment of {qrid}')
    payment_url     = f"{check_url}verifyslip/?QRid={qrid}&billerid={billerid}"
    res             = requests.get(payment_url)
    res_json        = res.json()
    print(res_json)
    #3)If Paid (resultCode=000) -- Update payment 
    # print ('Verify Success' if res_json['resultCode'] == '000' else 'Verify Failed')
    if res_json['resultCode'] == '000':
        # Successful (Found payment)
        date_time_obj       = datetime.strptime(res_json['transDate'], '%Y%m%d%H%M%S')
        order.paid          = True
        order.payment_ref   = res_json['bankRef']
        order.payment_date  = date_time_obj
        order.save()
        # update_order_payment(qrid,res_json['bankRef'],res_json['20201223104953'])

# -----------------------------------------------

def update_order_payment(qrid,bankref,transdate):
    # Update Order -->paid,payment_date,payment_ref
    # Get Order by qrid
    try:
        order = Order.objects.get(qrid=qrid)
        if order :
            print(transdate)
            date_time_obj = datetime.strptime(transdate, '%Y%m%d%H%M%S')

            order.paid = True
            order.payment_ref = bankref
            order.payment_date = date_time_obj
            order.save()
            # return True,'Update successful'
    except :
        # return False,'Error on Update payment function'
        pass