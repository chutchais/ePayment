# from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views
from .views import (OrderListView,OrderDetailView,
                    OrderUpdateSlip,OrderDeleteView,
                    OrderCreateView,get_booking_info,post_container,OrderUpdatePaid,
                    OrderUpdateExecuteJob,
                    ContainerListView,ContainerDetailView)

urlpatterns = [
    # path('', views.index, name='index'),
    path('containers',ContainerListView.as_view(),name='container-list'),
    path('containers/<pk>',ContainerDetailView.as_view(),name='container-detail'),
    path('',OrderListView.as_view(),name='list'),
    path('create',OrderCreateView.as_view(),name='create'),
    path('post_order',post_container,name='post_order'),
    path('booking/<booking>',get_booking_info,name='booking'),
    path('<pk>',OrderDetailView.as_view(),name='detail'),
    path('<pk>/payslip/',OrderUpdateSlip.as_view(),name='payslip'),
    path('<pk>/paid/',OrderUpdatePaid.as_view(),name='payment-confirm'),
    path('<pk>/execute/',OrderUpdateExecuteJob.as_view(),name='execute'),
    path('<pk>/delete/',OrderDeleteView.as_view(),name='delete'),


    # path('clear', views.clear_cart, name='cart_clear'),
    # path('create_order', views.create_order, name='create_order'),
    # url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    # url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]
