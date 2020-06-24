from django.conf.urls import url
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^clear$', views.cart_clear, name='cart_clear'),
    url(r'^add/(?P<product_id>\w+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\w+)/$', views.cart_remove, name='cart_remove'),
]

