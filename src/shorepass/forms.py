from django import forms
from .models import Shore

class ShorepassFile1Form(forms.ModelForm):
    class Meta:
        model = Shore
        fields = ['shorefile1']

class ShorepassFile2Form(forms.ModelForm):
    class Meta:
        model = Shore
        fields = ['shorefile2']