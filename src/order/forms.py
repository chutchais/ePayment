from django import forms
from .models import Order


class OrderPaySlipForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_slip']

class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_date','payment_ref']


class CreateOrderForm(forms.Form):
    booking 	= forms.CharField(label='Booking', max_length=100)
    wht 		= forms.BooleanField(required=False)
    charge 		= forms.CharField(max_length=10)
    vat_rate	= forms.CharField(max_length=10)
    wht_rate	= forms.CharField(max_length=10)
    grand_total = forms.CharField(max_length=10)
    containers 	= forms.CharField()
    address     = forms.IntegerField()