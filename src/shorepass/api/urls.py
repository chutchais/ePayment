# from django.conf.urls import url
from django.urls import path, include
from .views import (AgentList,AgentDetail,PodList,PodDetail,
                    get_voy_terminal,get_vessel_name_by_code,get_voy_by_vesselcode_voy)

urlpatterns = [
    path('agent/', AgentList.as_view()),
    path('agent/<int:pk>/', AgentDetail.as_view()),
    path('pod/', PodList.as_view()),
    path('pod/<int:pk>/', PodDetail.as_view()),
    path('voy/<terminal>/', get_voy_terminal), #get all voys by terminal (A0,B1)
    path('voy/<vessel_code>/<voy>/', get_voy_by_vesselcode_voy), #get voy detail by vessel code and voy
    path('vessel/<vessel_code>/', get_vessel_name_by_code), #get Vessel name by Vessel code
    

]
