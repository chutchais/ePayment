from django.shortcuts import render
from django.db.models import Q
from django.db.models import (ExpressionWrapper,F,Min,Max,Avg,StdDev,Count,Sum,
							Value, When,Case,IntegerField,CharField,FloatField)
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.db.models.functions import Floor,Ceil
from django.db.models.functions import Mod
from django.http import JsonResponse
from .models import Tariff
from oog.models import Oog
# Create your views here.

def is_OOG(booking,container):
    try:    
        oog = Oog.objects.get(booking=booking,container=container)
        if oog :
            return 'yes'
    except Exception as e:
        return 'no'
    return 'no'

def getTariff(request):
    category	 		= request.GET.get('category','E') #E = Export , I = Import
    full         		= request.GET.get('full','F') #F = FULL , E = Empty
    size         		= request.GET.get('size','40') #20,40,45
    
    # oog 				= request.GET.get('oog','no') #yes, no
    booking             = request.GET.get('booking','')
    container           = request.GET.get('container','')
    oog                 = is_OOG(booking,container)

    full_boolean        = True if full=='F' else False
    oog_boolean         = True if oog=='yes' else False
    size= size.replace('.00','')
    response = JsonResponse(get_tariff(category,full_boolean,size,oog_boolean), safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = '*'
    return response

def get_tariff_detail(category='E',full=True,size=40,oog=False):
    con_size= 'size20' if int(size)==20 else 'size40' if int(size)==40 else 'size45'
    tariff ={}
    sum_price = 0
    tariff_items = Tariff.objects.filter(   
        Q(container_profile__category='B')|Q(container_profile__category=category),
        container_profile__full=full,
        container_profile__oog=oog,
        container_profile__status = True,
        status= True
        ).order_by('seq')
                

    for x in tariff_items.values('title',con_size):
        tariff[x['title']]=x[con_size]

    if len(tariff) > 0 :
        sum_price = sum(v for k,v in tariff.items())
    
    return tariff

def get_tariff(category='E',full=True,size=40,oog=False):
    tariff_list = get_tariff_detail(category,full,size,oog)
    return tariff_list
