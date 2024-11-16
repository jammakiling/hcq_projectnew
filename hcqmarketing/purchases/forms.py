from django import forms
from .models import Purchase
from .models import PurchaseItem
from django.forms import modelformset_factory

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier']  # Only need supplier to create a purchase

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['inventory', 'quantity', 'price']
        widgets = {
            'inventory': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Make price readonly
        }

# Formset for purchase items
PurchaseItemFormSet = modelformset_factory(PurchaseItem, form=PurchaseItemForm, extra=1)
