from datetime import datetime
from .models import Order

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