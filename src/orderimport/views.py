from django.shortcuts import render
import urllib3
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.core.exceptions import ValidationError
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.views.generic.base import TemplateView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

# from .models import BillofLadding
from .models import Order,Container
from user_profile.models import Address
from tax.models import Tax
import json

# from .forms import BillofLaddingForm

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    paginate_by = 50
    def get_queryset(self):
        query = self.request.GET.get('q')
        # lacking_stock = self.request.GET.get('lacking')
        # over_stock = self.request.GET.get('over')
        print('Verify payment :',self.request.user.has_perm('order.verify_payment'))
        if query :
            return Order.objects.filter(Q(name__icontains=query) |
                                    Q(booking__name__icontains=query) ,
                                    user__username=self.request.user ).select_related('bl').order_by('-updated')

        if self.request.user.has_perm('orderimport.verify_payment') or  self.request.user.has_perm('orderimport.update_payment') :
            return Order.objects.all().select_related('bl').order_by('-updated')

        return Order.objects.filter(user__username=self.request.user).select_related('bl').order_by('-updated')
    
    def get_context_data(self,**kwargs):
        context = super(OrderListView,self).get_context_data(**kwargs)
        # context['addresses'] = Address.objects.filter(user__username=self.request.user)
        return context

class OrderDetailView(LoginRequiredMixin,DetailView):
    # model = Order
    queryset = Order.objects.select_related('bl','address')
    def get_context_data(self,**kwargs):
        context = super(OrderDetailView,self).get_context_data(**kwargs)
        # context['qr_url'] = settings.QR_CODE_ENDPOINT_URL#'http://10.24.50.91:8010/billing/'#
        context['qr_url'] = reverse_lazy('order:list')
        context['slip_verify_url'] = settings.SLIP_VERIFY_ENDPOINT_URL
        # For Container summary , SizeXCount(*) -- Total Price
        order = super().get_object()
        # summary = order.containers.values('cont_size').annotate(
        #         count=Count('container'),
        #         total_ex_vat= Sum('total') 
        #                         # + ((Sum('total')*order.vat_rate)/100) 
        #                         # - ((Sum('total')*order.wht_rate)/100) if order.wht else 0
        #         )
        # context['summary'] = summary
        # for c in obj.containers.all():
        #     print(c)
        return context