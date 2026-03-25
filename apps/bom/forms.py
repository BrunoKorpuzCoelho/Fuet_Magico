from django import forms
from .models import ProductBOM


class ProductBOMForm(forms.ModelForm):
    class Meta:
        model = ProductBOM
        fields = [
            'product',
            'internal_reference',
            'qty_produced',
            'uom',
            'owner_company',
            'notes',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select',
            }),
            'internal_reference': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: BOM-001',
                'maxlength': '64',
            }),
            'qty_produced': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '1.0000',
                'step': '0.0001',
                'min': '0.0001',
            }),
            'uom': forms.Select(attrs={
                'class': 'form-select',
            }),
            'owner_company': forms.Select(attrs={
                'class': 'form-select',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Instruções de preparação, anotações...',
                'rows': 4,
            }),
        }
