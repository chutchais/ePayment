from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from order.services import update_order_payment
# Added on Dec 4,2020 -- To update payment to import order and enable Queue
from orderimport.services import update_import_payment
from django_q.tasks import async_task

@api_view(['GET', 'POST'])
def update_payment(request):
    import environ
    # reading .env file
    env = environ.Env()
    environ.Env.read_env()

    SECRET_KEY = env('SECRET_KEY')
    if request.method == 'POST':
        if request.data['token'] == SECRET_KEY :
            qrid        = request.data['QRId']
            bankref     = request.data['BankRef']
            transdate   = request.data['TransDate']
            # Modify on Dec 4,2020 -- To add payment for Import and enable Queue.
            # update_order_payment (qrid,bankref,transdate)
            # update_import_payment(qrid,bankref,transdate)
            async_task('order.services.update_order_payment',qrid,bankref,transdate)
            async_task('orderimport.services.update_import_payment',qrid,bankref,transdate)
            # End payment update 

            return JsonResponse({"result":True,"message": "Update payment successful"})
        else:
            return JsonResponse({"result":False,"message":"Key is not match"})
    return JsonResponse({"message":"ePayment Update Service"})