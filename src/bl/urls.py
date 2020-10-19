from django.urls import path, include
from . import views
from .views import index,container,get_bl_info,get_container_info

urlpatterns = [
    path('', index, name='home'),
    path('report',index,name='report'),
    path('report/<bl>',index,name='report-bl'),
    path('container',container,name='container'),
    path('api/bl/<bl>',get_bl_info,name='bl'),
    path('api/container/<container>',get_container_info,name='container'),
    ]