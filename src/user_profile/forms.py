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
    class Meta:
        model = Address
        fields = ['company','address','tax']
