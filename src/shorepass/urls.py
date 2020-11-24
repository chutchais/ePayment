# from django.conf.urls import url
from django.urls import path, include

from .views import (ShoreListView,ShoreDetailView,ShoreCreateView)

urlpatterns = [
    path('',ShoreListView.as_view(), name='list') ,
    path('create',ShoreCreateView.as_view(), name='create') ,
    path('<pk>',ShoreDetailView.as_view(), name='shoredetail') ,
]
