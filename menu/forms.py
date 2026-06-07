from .models import Product
from django import forms



class AddItemForm(forms.Form):

    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True)
    )

    quantity = forms.IntegerField(min_value=1)

    