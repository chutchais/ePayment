from django import forms
from .models import BillofLadding

import re

class BillofLaddingForm(forms.ModelForm):
    class Meta:
        model = BillofLadding
        fields = ['name','declaration']
    
    def clean_declaration(self):
        declaration = self.cleaned_data['declaration']
        if not re.match("A[0-9]{13}$", declaration) :
            raise forms.ValidationError("กรุณากรอกเลขใบขน หรือ เลขใบขนผิดฟอร์แมตท์")
        return declaration