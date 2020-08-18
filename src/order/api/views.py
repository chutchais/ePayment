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
        if request.data['key'] == SECRET_KEY :
            update_order_payment ('','','')
            return JsonResponse({"result":True,"message": "", "data": request.data})
        else:
            return JsonResponse({"result":False,"message":"Key is not match"})
    return JsonResponse({"message":SECRET_KEY})