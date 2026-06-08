from .models import Product
from django import forms



class AddItemForm(forms.Form):

    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        widget=forms.HiddenInput()
    )

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.HiddenInput()
    )

    