from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.views.generic.base import TemplateView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect
# Create your views here.

from .models import Booking
from user_profile.models import Address
from tax.models import Tax
import json

from order.models import Order,Container
from django.http import Http404

# Added on Dec 8,2020 -- To limit time access from user
from utility.mixin import TimeLimitMixin

class BookingListView(LoginRequiredMixin,ListView):
	model = Booking
	paginate_by = 30
	def get_queryset(self):
		query = self.request.GET.get('q')
		# lacking_stock = self.request.GET.get('lacking')
		# over_stock = self.request.GET.get('over')

		# print(settings.EXPORT_BOOKING_ENDPOINT_URL)

		if query :
			return Booking.objects.filter(Q(name__icontains=query),
									user__username=self.request.user ).select_related('user').order_by('-updated')
		return Booking.objects.filter(user__username=self.request.user).select_related('user').order_by('-updated')
	
	def get_context_data(self,**kwargs):
		context = super(BookingListView,self).get_context_data(**kwargs)
		context['addresses'] = Address.objects.filter(user__username=self.request.user)
		# context['export_booking_url'] = settings.EXPORT_BOOKING_ENDPOINT_URL.strip()
		return context

class BookingDetailView(TimeLimitMixin,LoginRequiredMixin,DetailView):
	model = Booking
	def get_context_data(self,**kwargs):
		context = super(BookingDetailView,self).get_context_data(**kwargs)
		context['tax'] = Tax.objects.get(name='Default')

		# context['addresses_items'] = json.dumps(list(Address.objects.filter(
		# 							user__username=self.request.user
		# 							).order_by('company').values('pk', 'company','address','tax'))).replace('\\r\\n',' ')
		# http://192.168.10.16:5001/booking/
		booking_url = f"{reverse_lazy('order:list')}booking/"
		# print (f"{reverse_lazy('order:list')}booking/")
		context['export_booking_url'] = booking_url#settings.EXPORT_BOOKING_ENDPOINT_URL
		
		# Added on Nov 9,2020 -- To prevent choose Container that are under processing.
		booking 					= context['object']
		
		# Modify on Dec 23,2020 -- To do not allow process on Container that already exist in Order
		# orders 					= Order.objects.filter(booking=booking,paid=False)
		orders 						= Order.objects.filter(booking__name=booking,execute_job=False)
		# print('Booking details' , booking,orders)
		containers 					= Container.objects.filter(order__in = orders)
		context['onprogressing'] 	= json.dumps(list(containers.values_list('container',flat=True)))

		# Added on Nov 17,2020 -- To provide Vessel Name url (on shorepass app)
		vessel_url 					= f"{reverse_lazy('shoreapi:index')}vessel/"
		context['vessel_url'] 		= vessel_url

		# Added on Nov 17,2020 -- To provide Address url (on user_profile)
		address_url 				= f"{reverse_lazy('profileapi:index')}address/"
		context['address_url'] 		= address_url
		return context


class BookingDetailQueryView(TemplateView):
	template_name = "booking/booking_query.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tax'] = Tax.objects.get(name='Default')
		booking_url = f"{reverse_lazy('order:list')}booking/"
		context['export_booking_url'] = booking_url
		# Added on Nov 17,2020 -- To provide Vessel Name url (on shorepass app)
		vessel_url 					= f"{reverse_lazy('shoreapi:index')}vessel/"
		context['vessel_url'] 		= vessel_url
		# Added on Nov 17,2020 -- To provide Address url (on user_profile)
		address_url 				= f"{reverse_lazy('profileapi:index')}address/"
		context['address_url'] 		= address_url
		return context

class BookingCreateView(TimeLimitMixin,LoginRequiredMixin,CreateView):
	model = Booking
	# fields = ['name','terminal']
	fields = ['name']
	success_url = reverse_lazy('booking:list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		try:
			# Added on Aug 25,2020 -- To convert to capital char.
			form.instance.name = form.instance.name.upper()
			form.save()  # should raise an exception if unique_together constrain fails
		except :
			form.add_error('name', 'Booking already Exist!')  # add custom error to form
			return self.form_invalid(form)  # return the invalid form
		return super(BookingCreateView, self).form_valid(form)

class BookingDeleteView(LoginRequiredMixin,DeleteView):
	model = Booking
	success_url = reverse_lazy('booking:list')

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if (self.object.user == request.user) or request.user.is_superuser or request.user.is_staff :
			self.object.delete()
			return redirect(self.get_success_url())
		else:
			raise Http404("Not allow to delete") #or return HttpResponse('404_url')