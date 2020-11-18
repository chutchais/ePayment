# from django.conf.urls import url
from django.urls import path, include
from .views import (AgentList,AgentDetail,PodList,PodDetail,
                    get_voy_terminal,get_vessel_name_by_code,get_voy_by_vesselcode_voy,
                    CustomerList,CustomerDetail)

urlpatterns = [
    path('', PodList.as_view(),name='index'),
    path('agent/', AgentList.as_view(),name='agent'),
    path('agent/<int:pk>/', AgentDetail.as_view(),name='agent-detail'),
    path('pod/', PodList.as_view(),name='pod'),
    path('pod/<int:pk>/', PodDetail.as_view(),name='pod-detail'),
    path('customer/', CustomerList.as_view(),name='customer'),
    path('customer/<int:pk>/', CustomerDetail.as_view(),name='customer-detail'),
    path('voy/<terminal>/', get_voy_terminal,name='voy'), #get all voys by terminal (A0,B1)
    path('voy/<vessel_code>/<voy>/', get_voy_by_vesselcode_voy,name='voy-detail'), #get voy detail by vessel code and voy
    path('vessel/<vessel_code>/', get_vessel_name_by_code,name='vessel'), #get Vessel name by Vessel code
    

]
