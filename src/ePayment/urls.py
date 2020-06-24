"""ePayment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user_profile import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

# from order.views import index

urlpatterns = [
	
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('booking/',include(('booking.urls','booking'), namespace='booking')),
    path('user_profile/', include('user_profile.urls',namespace='user_profile')),
    path('order/',include(('order.urls','order'), namespace='order')),
    # Sign-up pattern
    path('signup/', views.signup, name='signup'),
    path('auth/profile_setting/', views.profileSetting, name='profile_setting'),
    path('auth/change_password/', 
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',
        success_url='/auth/password_change/done/'), 
        name='change_password'),
    path('change_password_done/', 
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='change_password_done'),
    path('auth/password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
        success_url='done/'), 
        name="password_reset"),
    path('auth/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name="password_reset_done"),
    path('auth/reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
        success_url='/auth/reset/done/'),
        name="password_reset_confirm"),
    path('auth/reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
        name="password_reset_complete"),
    path('auth/account_activation_sent/', 
        views.account_activation_sent, name='account_activation_sent'),
    
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #     views.activate, name='activate'),
    # path('cart/', include('cart.urls',namespace='cart')),
    path('tariff/', include('tariff.urls',namespace='tariff')),
    # path('',include('order.urls')),
    # Home pattern
    # path('home/', TemplateView.as_view(template_name='home.html'),name='home'),
    path('', include(('order.urls','order'), namespace='home') ,name='home'),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.conf import settings
# from django.urls import include, path

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns