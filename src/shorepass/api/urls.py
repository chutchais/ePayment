# from django.conf.urls import url
from django.urls import path, include
from .views import (AgentList,AgentDetail,PodList,PodDetail,get_2weeks_berth_info)

urlpatterns = [
    path('agent/', AgentList.as_view()),
    path('agent/<int:pk>/', AgentDetail.as_view()),
    path('pod/', PodList.as_view()),
    path('pod/<int:pk>/', PodDetail.as_view()),
    path('berth/<terminal>/', get_2weeks_berth_info),

]
