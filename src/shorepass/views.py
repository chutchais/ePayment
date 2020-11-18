from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Shore

class ShoreListView(LoginRequiredMixin,ListView):
    model = Shore
    paginate_by = 50
    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     # lacking_stock = self.request.GET.get('lacking')
    #     # over_stock = self.request.GET.get('over')
    #     print('Verify payment :',self.request.user.has_perm('order.verify_payment'))
    #     if query :
    #         if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
    #             return Order.objects.filter(Q(name__icontains=query) |
    #                                     Q(booking__name__icontains=query)).select_related('booking').order_by('-updated')
    #         else:
    #             return Order.objects.filter(Q(name__icontains=query) |
    #                                     Q(booking__name__icontains=query) ,
    #                                     user__username=self.request.user ).select_related('booking').order_by('-updated')

    #     if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
    #         return Order.objects.all().select_related('booking').order_by('-updated')[:200]

    #     return Order.objects.filter(user__username=self.request.user).select_related('booking').order_by('-updated')[:200]
    
    # def get_context_data(self,**kwargs):
    #     context = super(OrderListView,self).get_context_data(**kwargs)
    #     # context['addresses'] = Address.objects.filter(user__username=self.request.user)
    #     return context

class ShoreDetailView(LoginRequiredMixin,DetailView):
    model = Shore


class ShoreCreateView(LoginRequiredMixin,CreateView):
    model = Shore
    fields = ['booking','vessel_name','pod','voy','terminal','agent']

# class ShoreCreateView(TemplateView):
# 	template_name = "shorepass/shore_create.html"

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['tax'] = Tax.objects.get(name='Default')
# 		booking_url = f"{reverse_lazy('order:list')}booking/"
# 		context['export_booking_url'] = booking_url
# 		# Added on Nov 17,2020 -- To provide Vessel Name url (on shorepass app)
# 		vessel_url 					= f"{reverse_lazy('shoreapi:index')}vessel/"
# 		context['vessel_url'] 		= vessel_url
# 		# Added on Nov 17,2020 -- To provide Address url (on user_profile)
# 		address_url 				= f"{reverse_lazy('profileapi:index')}address/"
# 		context['address_url'] 		= address_url
# 		return context