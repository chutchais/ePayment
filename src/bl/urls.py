from django.urls import path, include
from . import views
from .views import index,get_bl_info

urlpatterns = [
    path('', index, name='home'),
    path('report',index,name='report'),
    path('api/bl/<bl>',get_bl_info,name='bl'),
    ]