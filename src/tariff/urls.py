from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from .views import getTariff

app_name = 'tariff'

urlpatterns = [
	# Page
	path('',getTariff,name='detail'),
]