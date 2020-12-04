from django.urls import path, include
from .views import (OrderListView,OrderDetailView,
                    OrderDeleteView,post_container,
                    OrderUpdateSlip,OrderUpdateWHT,OrderUpdateDo,
                    OrderUpdateExecuteJob,OrderUpdatePaid)

urlpatterns = [
    # Guess access
    # path('report',index,name='report'),
    # path('report/<bl>',index,name='report-bl'),
    # path('container',container,name='container'),

    # Member access
    path('', OrderListView.as_view(), name='list'),
    # path('create',BillofLaddingCreateView.as_view(),name='create'),
    path('post_order',post_container,name='post_order'),
    path('<pk>',OrderDetailView.as_view(),name='detail'),
    path('<pk>/payslip/',OrderUpdateSlip.as_view(),name='payslip'),
    path('<pk>/whtslip/',OrderUpdateWHT.as_view(),name='whtslip'),
    path('<pk>/do/',OrderUpdateDo.as_view(),name='do'),
    path('<pk>/delete/',OrderDeleteView.as_view(),name='delete'),

    # path('<pk>/whtslip/',OrderUpdateWHT.as_view(),name='whtslip'),
    path('<pk>/paid/',OrderUpdatePaid.as_view(),name='payment-confirm'),
    path('<pk>/execute/',OrderUpdateExecuteJob.as_view(),name='execute'),


     
    
    # path('api/bl/<bl>',get_bl_info,name='bl'),
    # path('api/container/<container>',get_container_info,name='container'),
    ]