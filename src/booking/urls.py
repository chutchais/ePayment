from django.urls import path, include
from . import views
from django.views.decorators.cache import cache_page
from .views import BookingListView,BookingCreateView,BookingDetailView,BookingDeleteView

urlpatterns = [
    # path('', views.index, name='index'),
    path('',BookingListView.as_view(),name='list'),
    path('create',BookingCreateView.as_view(),name='create'),
    # path('booking/<booking>',get_booking_info,name='booking'),
    path('<pk>',BookingDetailView.as_view(),name='detail'),
    # path('<pk>/payslip/',OrderUpdateSlip.as_view(),name='payslip'),
    path('<pk>/delete/',BookingDeleteView.as_view(),name='delete'),
    ]