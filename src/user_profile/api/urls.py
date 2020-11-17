# from django.conf.urls import url
from django.urls import path, include
from .views import (AddressList,AddressDetail)

urlpatterns = [
    path('', AddressList.as_view(),name='index'),
    path('address/', AddressList.as_view(),name='address-list'),
    path('address/<int:pk>/', AddressDetail.as_view(),name='address-detail'),
]
