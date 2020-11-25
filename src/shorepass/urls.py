# from django.conf.urls import url
from django.urls import path, include

from .views import (ShoreListView,ShoreDetailView,
                    ShoreCreateView,ShoreUpdateFile1,ShoreUpdateFile2,
                    ShoreDeleteView,ShoreUpdateExecuteJob,ShoreUpdateContactMessage)

urlpatterns = [
    path('',ShoreListView.as_view(), name='list') ,
    path('create',ShoreCreateView.as_view(), name='create') ,
    path('<pk>',ShoreDetailView.as_view(), name='shoredetail') ,
    path('<pk>/file1/',ShoreUpdateFile1.as_view(),name='file1'),
    path('<pk>/file2/',ShoreUpdateFile2.as_view(),name='file2'),
    path('<pk>/delete/',ShoreDeleteView.as_view(),name='shoredelete'),
    path('<pk>/execute/',ShoreUpdateExecuteJob.as_view(),name='execute'),
    path('<pk>/message/',ShoreUpdateContactMessage.as_view(),name='message'),
]
