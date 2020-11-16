from django.shortcuts import render, redirect

# Create your views here.

# from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import (SignUpForm,ProfileSettingForm,
					ProfileAvartarForm,ProfileIDcardForm,
					ProfileSigForm,AddressForm,ContactForm)
from .models import Profile,Address

from .tokens import account_activation_token

def profileSetting(request):
	if request.method == 'POST':
		formavatar = ProfileSettingForm(request.POST, request.FILES)
		if formavatar.is_valid():
			profile = Profile.objects.get(user=request.user)
			if 'avartar' in request.FILES :
				profile.avartar = request.FILES['avartar']
			if 'idcard' in request.FILES :
				profile.idcard = request.FILES['idcard']
			if 'signature' in request.FILES :
				profile.signature = request.FILES['signature']
			
			if 'lineid' in request.POST :
				if request.POST['lineid']:
					profile.lineid = request.POST['lineid']
			
			if 'phone' in request.POST :
				if request.POST['phone']:
					profile.phone = request.POST['phone']
			
			profile.save()
		# Added on Nov 2,2020 -- To save LindId and Telephone number
		
			return redirect('profile_setting')
	else:
		# form            = ProfileSettingForm()
		fromAvatar      = ProfileAvartarForm()
		formidcard      = ProfileIDcardForm()
		formsignature   = ProfileSigForm()
		formaddress     = AddressForm()
		formContact		= ContactForm()
		profile = Profile.objects.get(user=request.user)
	return render(request, 'registration/profile.html', {'formavatar':fromAvatar,
													'formidcard':formidcard,
													'formsignature':formsignature,
													'formaddress':formaddress,
													'formcontact':formContact,
													'profile': profile})

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			print('Start Signup')
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your LCB1 ePayment Account'
			to_email = form.cleaned_data.get('email')
			message = render_to_string('registration/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			# print(message)
			user.email_user(subject, message)
			return redirect('account_activation_sent')
			# Created then auto Login
			# form.save()
			# username = form.cleaned_data.get('username')
			# raw_password = form.cleaned_data.get('password1')
			# user = authenticate(username=username, password=raw_password)
			# login(request, user)
			# return redirect('/home')
			# -------------
			
			
	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html', {'form': form})

def account_activation_sent(request):
	return render(request, 'registration/activation_sent.html')

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.email_confirmed = True
		user.save()
		login(request, user)
		return redirect('/home')
	else:
		return render(request, 'registration/account_activation_invalid.html')

@login_required
def add_address(request):
	upload = AddressForm()
	if request.method == 'POST':
		upload = AddressForm(request.POST, request.FILES)
		if upload.is_valid():
			profile = upload.save(commit=False)
			user = User.objects.get(username=request.user)
			print ('Current user',user)
			profile.user = user
			
			profile.save()
			return redirect('profile_setting')
		else:
			# return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
			return render(request, 'profile/address.html', {'address_form':upload})
	else:
		return render(request, 'profile/address.html', {'address_form':upload})

@login_required
def update_address(request, address_id):
	address_id = int(address_id)
	try:
		address_sel = Address.objects.get(id = address_id,user__username= request.user)

	except Address.DoesNotExist:
		return redirect('/home')
	address_form = AddressForm(request.POST or None, instance = address_sel)
	if address_form.is_valid():
	   address_form.save()
	   return redirect('profile_setting')
	return render(request, 'profile/address.html', {'address_form':address_form})


class AddressDeleteView(LoginRequiredMixin,DeleteView):
	model = Address
	success_url = reverse_lazy('profile_setting')
	
	# def delete(self, request, *args, **kwargs):
	# 	self.object = self.get_object()
	# 	if (self.object.user == request.user) or request.user.is_superuser or request.user.is_staff :
	# 		self.object.delete()
	# 		return redirect(self.get_success_url())
	# 	else:
	# 		raise Http404("Not allow to delete") #or return HttpResponse('404_url')

# @login_required
# def delete_address(request, address_id):
# 	address_id = int(address_id)
# 	try:
# 		address_sel = Address.objects.get(id = address_id,user__username= request.user)
# 	except Address.DoesNotExist:
# 		return redirect('/home')
# 	address_sel.delete()
# 	return redirect('profile_setting')



# class ProfileListView(ListView):
# 	model = Profile
# 	paginate_by = 50
	# def get_queryset(self):
	# 	query = self.request.GET.get('q')
	# 	# lacking_stock = self.request.GET.get('lacking')
	# 	# over_stock = self.request.GET.get('over')
	# 	if query :
	# 		return Profile.objects.filter(user__name = query).order_by('user')

	# 	# if self.request.user.has_perm('order.verify_payment') or  self.request.user.has_perm('order.update_payment') :
	# 	#     return Order.objects.all().order_by('-updated')

	# 	return Profile.objects.all().order_by('user')
	
	# def get_context_data(self,**kwargs):
	#     context = super(ProfileListView,self).get_context_data(**kwargs)
	#     # context['addresses'] = Address.objects.filter(user__username=self.request.user)
	#     return context