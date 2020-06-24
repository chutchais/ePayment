from django.urls import path
from . import views


app_name='profile'

urlpatterns = [
    # path('', views.index, name = 'index'),
    # path('',views.ProfileListView.as_view(),name='list'),
    path('add/', views.add_address, name = 'add'),
    path('update/<int:address_id>', views.update_address,name = 'update'),
    path('delete/<int:address_id>', views.delete_address,name = 'delete')
]