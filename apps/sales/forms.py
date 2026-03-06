from django import forms
from .models import SaleOrder, SaleOrderLine, PaymentTerm


class SaleOrderForm(forms.ModelForm):
    """Header form for SaleOrder (client, document_type, dates, notes)."""

    class Meta:
        model = SaleOrder
        fields = [
            'client',
            'order_date',
            'delivery_date',
            'payment_terms',
            'amount_paid',
            'notes',
        ]
        widgets = {
            'order_date':    forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'notes':         forms.Textarea(attrs={'rows': 3}),
        }


class PaymentTermForm(forms.ModelForm):
    """Form for creating/editing a PaymentTerm (sales)."""

    class Meta:
        model = PaymentTerm
        fields = ['name', 'days', 'description', 'is_default']


class SaleOrderLineForm(forms.ModelForm):
    """Form for adding/editing a single sale order line."""

    class Meta:
        model = SaleOrderLine
        fields = [
            'product',
            'uom',
            'quantity',
            'unit_price',
            'tax_rate',
            'notes',
        ]
