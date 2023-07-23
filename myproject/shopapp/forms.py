from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'discount'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'products', 'promocode', 'user'
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'products': forms.CheckboxSelectMultiple(),
        }
