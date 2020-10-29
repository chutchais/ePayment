from django.urls import path, include
from . import views
from .views import (BillofLaddingListView,
                BillofLaddingDetailView,
                BillofLaddingCreateView,
                BillofLaddingDeleteView,
                index,container,get_bl_info,get_container_info)

urlpatterns = [
    # Guess access
    path('report',index,name='report'),
    path('report/<bl>',index,name='report-bl'),
    path('container',container,name='container'),

    # Member access
    path('', BillofLaddingListView.as_view(), name='list'),
    path('create',BillofLaddingCreateView.as_view(),name='create'),
    path('<pk>',BillofLaddingDetailView.as_view(),name='detail'),
    path('<pk>/delete/',BillofLaddingDeleteView.as_view(),name='delete'),

    
    path('api/bl/<bl>',get_bl_info,name='bl'),
    path('api/container/<container>',get_container_info,name='container'),
    ]