from django import forms
from .models import PurchaseOrder, PurchaseOrderLine, PaymentTerm


class PaymentTermForm(forms.ModelForm):
    """Form for creating/editing a PaymentTerm."""

    class Meta:
        model = PaymentTerm
        fields = ['name', 'days', 'description', 'is_default']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class PurchaseOrderForm(forms.ModelForm):
    """Header form for PurchaseOrder (supplier, dates, notes)."""

    class Meta:
        model = PurchaseOrder
        fields = [
            'supplier',
            'order_date',
            'expected_delivery_date',
            'payment_terms',
            'origin',
            'notes',
        ]
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class PurchaseOrderLineForm(forms.ModelForm):
    """Form for adding/editing a single line."""

    class Meta:
        model = PurchaseOrderLine
        fields = [
            'product',
            'uom',
            'quantity',
            'unit_price',
            'tax_rate',
            'notes',
        ]
