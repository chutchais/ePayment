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

from .models import BillofLadding
from user_profile.models import Address
from tax.models import Tax
import json

from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import BillofLaddingForm

class BillofLaddingListView(LoginRequiredMixin,ListView):
	model = BillofLadding
	paginate_by = 30
	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return BillofLadding.objects.filter(Q(name__icontains=query),
									user__username=self.request.user ).select_related('user').order_by('-updated')
		return BillofLadding.objects.filter(
				user__username=self.request.user).select_related('user').order_by('-updated')
	
	def get_context_data(self,**kwargs):
		context = super(BillofLaddingListView,self).get_context_data(**kwargs)
		context['addresses'] = Address.objects.filter(user__username=self.request.user)
		# context['export_booking_url'] = settings.EXPORT_BOOKING_ENDPOINT_URL.strip()
		return context

class BillofLaddingDetailView(LoginRequiredMixin,DetailView):
	model = BillofLadding
	def get_context_data(self,**kwargs):
		context = super(BillofLaddingDetailView,self).get_context_data(**kwargs)
		context['tax'] = Tax.objects.get(name='Default')
		# context['addresses'] = Address.objects.filter(user__username=self.request.user)
		# context['addresses_items'] = json.dumps(list(Address.objects.filter(
		# 							user__username=self.request.user
		# 							).order_by('company').values('pk', 'company','address','tax'))).replace('\\r\\n',' ')
		# http://192.168.10.16:5001/booking/
		bl_url = f"{reverse_lazy('bl:list')}"
		# print (f"{reverse_lazy('order:list')}booking/")
		context['import_url'] = f'{bl_url}api/bl/'#settings.EXPORT_BOOKING_ENDPOINT_URL
		
		# Added on Dec 1,2020 -- To provide Address url (on user_profile)
		address_url 				= f"{reverse_lazy('profileapi:index')}address/"
		context['address_url'] 		= address_url
		return context

		def dispatch(self, request, *args, **kwargs):
			obj = self.get_object()
			user_obj = self.request.user
			if user_obj.is_staff or user_obj.is_superuser :
				return super().dispatch(request,*args,**kwargs)

			if not obj.user == self.request.user :
				raise PermissionDenied
			return super().dispatch(request,*args,**kwargs)

class BillofLaddingCreateView(LoginRequiredMixin,CreateView):
	# model = BillofLadding
	# fields = ['name','declaration']
	template_name = 'bl/billofladding_form.html'
	form_class = BillofLaddingForm
	success_url = reverse_lazy('bl:list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		try:
			# Added on Aug 25,2020 -- To convert to capital char.
			form.instance.name = form.instance.name.upper()
			form.save()  # should raise an exception if unique_together constrain fails
		except :
			form.add_error('name', 'BL already Exist!')  # add custom error to form
			return self.form_invalid(form)  # return the invalid form
		return super(BillofLaddingCreateView, self).form_valid(form)

class BillofLaddingDeleteView(DeleteView):
	model = BillofLadding
	success_url = reverse_lazy('bl:list')

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		user_obj = self.request.user
		if user_obj.is_staff or user_obj.is_superuser :
			return super().dispatch(request,*args,**kwargs)

		if not obj.user == self.request.user :
			raise PermissionDenied
		return super().dispatch(request,*args,**kwargs)


# Create your views here.
def index(request,bl=''):
	context = {}
	bl_url = f"{reverse_lazy('bl:list')}"
	# print(bl_url)
		# print (f"{reverse_lazy('order:list')}booking/")
	context['import_bl_url'] = f'{bl_url}api/bl/'
	context['bl'] = bl
	return render(request, 'bl/index.html', context=context)

def container(request):
	context = {}
	bl_url = f"{reverse_lazy('bl:list')}"
	# print(bl_url)
		# print (f"{reverse_lazy('order:list')}booking/")
	context['import_container_url'] = f'{bl_url}api/container/'
	return render(request, 'bl/container.html', context=context)


def get_bl_info(request,bl):
	import json
	http = urllib3.PoolManager()
	# print ('get_booking_info')
	r = http.request('GET', f'http://192.168.10.16:5000/bl/{bl}')
	# return json.loads(r.data.decode('utf-8'))
	response = JsonResponse(json.loads(r.data.decode('utf-8')), safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response

# Added on Oct 16,2020 -- To support Import container info API
def get_container_info(request,container):
	import json
	http = urllib3.PoolManager()
	# print ('get_booking_info')
	r = http.request('GET', f'http://192.168.10.16:5000/container/{container}')
	# return json.loads(r.data.decode('utf-8'))
	response = JsonResponse(json.loads(r.data.decode('utf-8')), safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response
