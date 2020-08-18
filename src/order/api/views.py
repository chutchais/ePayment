from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from order.services import update_order_payment

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
            update_order_payment (qrid,bankref,transdate)
            return JsonResponse({"result":True,"message": "Update payment successful"})
        else:
            return JsonResponse({"result":False,"message":"Key is not match"})
    return JsonResponse({"message":"ePayment Update Service"})