from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Address

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ProfileSettingForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avartar','idcard','signature']

class ProfileAvartarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avartar']

class ProfileIDcardForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['idcard']

class ProfileSigForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['signature']

class AddressForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Address
        fields = ['company','address','branch','tax']
    
    def clean_company(self):
        company = self.cleaned_data['company']
        company = company.translate({ord(c): None for c in "'"})
        return company

    def clean_address(self):
        address = self.cleaned_data['address']
        address = address.translate({ord(c): None for c in "'!@#$"})
        return address
    
    def clean_branch(self):
        branch = self.cleaned_data['branch']
        branch = branch.translate({ord(c): None for c in "'!@#$"})
        return branch

    def clean_tax(self):
        tax = self.cleaned_data['tax']
        tax = tax.translate({ord(c): None for c in "'!@#$"})
        return tax

class ContactForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['lineid','phone']
    
    def get_form_kwargs(self):
        kwargs = super(ContactForm, self).get_form_kwargs()
        # kwargs['initial'] = {'lineid':'tuk','phone':'0999999'}  # your initial data here
        return kwargs