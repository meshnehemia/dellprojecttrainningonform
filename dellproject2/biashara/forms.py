from django import forms
from biashara.models import Product


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'origin', 'color']


class MpesapaymentForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=12, label="phone number")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="amount")
