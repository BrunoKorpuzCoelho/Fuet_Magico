from django import forms
from django.db import models
from .models import Category, UoM, UoMCategory, Product, Warehouse, StockMovement


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Farinhas',
                'maxlength': '128',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Descrição da categoria...',
                'rows': 4,
            }),
            'parent': forms.Select(attrs={
                'class': 'form-input',
            }),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter parent choices to same company (or global)
        qs = Category.objects.filter(is_active=True).order_by('name')
        if company:
            qs = qs.filter(
                models.Q(owner_company=company) | models.Q(owner_company__isnull=True)
            )
        # Exclude self to prevent circular parent
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            # Also exclude descendants
            descendants = self._get_descendants(self.instance)
            if descendants:
                qs = qs.exclude(pk__in=descendants)
        self.fields['parent'].queryset = qs
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '— Sem categoria pai (raiz) —'

    @staticmethod
    def _get_descendants(category):
        """Return all descendant IDs to prevent circular references."""
        descendants = []
        children = list(Category.objects.filter(parent=category).values_list('id', flat=True))
        while children:
            descendants.extend(children)
            children = list(
                Category.objects.filter(parent_id__in=children).values_list('id', flat=True)
            )
        return descendants


class UoMForm(forms.ModelForm):
    class Meta:
        model = UoM
        fields = ['name', 'symbol', 'category', 'uom_type', 'factor', 'rounding']

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter category choices to same company (or global)
        qs = UoMCategory.objects.filter(is_active=True).order_by('name')
        if company:
            qs = qs.filter(
                models.Q(owner_company=company) | models.Q(owner_company__isnull=True)
            )
        self.fields['category'].queryset = qs
        self.fields['category'].empty_label = '— Selecionar categoria —'


class UoMCategoryForm(forms.ModelForm):
    class Meta:
        model = UoMCategory
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'internal_reference', 'reference', 'barcode',
            'product_type', 'category',
            'uom', 'uom_purchase', 'conversion_loss_pct',
            'sale_price', 'cost_price', 'tax_rate',
            'description', 'image',
            'min_stock', 'is_manufactured',
        ]

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter category choices by company
        cat_qs = Category.objects.filter(is_active=True).order_by('name')
        if company:
            cat_qs = cat_qs.filter(
                models.Q(owner_company=company) | models.Q(owner_company__isnull=True)
            )
        self.fields['category'].queryset = cat_qs
        self.fields['category'].required = False
        self.fields['category'].empty_label = '— Selecionar categoria —'

        # Filter UoM choices by company
        uom_qs = UoM.objects.filter(is_active=True).select_related('category').order_by('category__name', 'name')
        if company:
            uom_qs = uom_qs.filter(
                models.Q(owner_company=company) | models.Q(owner_company__isnull=True)
            )
        self.fields['uom'].queryset = uom_qs
        self.fields['uom'].empty_label = '— Selecionar UdM —'

        self.fields['uom_purchase'].queryset = uom_qs
        self.fields['uom_purchase'].required = False
        self.fields['uom_purchase'].empty_label = '— Mesma que UdM principal —'

        self.fields['conversion_loss_pct'].required = False
        self.fields['conversion_loss_pct'].widget.attrs.update({
            'class': 'form-input w-full',
            'step': '0.01',
            'min': '0',
            'max': '100',
            'placeholder': '0',
        })

        # Style min_stock widget
        self.fields['min_stock'].required = False
        self.fields['min_stock'].widget.attrs.update({
            'class': 'form-input w-full',
            'step': '0.001',
            'min': '0',
            'placeholder': '0',
        })


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'code', 'address', 'is_default']

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['code'].required = True
        self.fields['address'].required = False


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'adjustment_direction', 'scrap_reason', 'warehouse', 'partner', 'date', 'origin', 'notes']

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Warehouse: filter by company
        wh_qs = Warehouse.objects.filter(is_active=True)
        if company:
            wh_qs = wh_qs.filter(
                models.Q(owner_company=company) | models.Q(owner_company__isnull=True)
            )
        self.fields['warehouse'].queryset = wh_qs
        self.fields['warehouse'].empty_label = '— Selecionar armazém —'

        # Partner (contacts): filter by company
        from apps.contacts.models import Contact
        partner_qs = Contact.objects.filter(is_active=True).order_by('name')
        if company:
            partner_qs = partner_qs.filter(
                models.Q(owner_company=company) | models.Q(owner_company__isnull=True)
            )
        self.fields['partner'].queryset = partner_qs
        self.fields['partner'].required = False
        self.fields['partner'].empty_label = '— Nenhum parceiro —'

        # Date: HTML5 datetime-local widget
        self.fields['date'].widget = forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        )
        self.fields['date'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']

        # Optional fields
        self.fields['origin'].required = False
        self.fields['notes'].required = False
        self.fields['adjustment_direction'].required = False  # validated in clean()
        self.fields['scrap_reason'].required = False  # validated in clean()

    def clean(self):
        cleaned_data = super().clean()
        movement_type = self.data.get('movement_type') or cleaned_data.get('movement_type', '')
        if movement_type == 'adjustment' and not cleaned_data.get('adjustment_direction'):
            self.add_error('adjustment_direction', 'Selecione a direção do ajuste (Entrada ou Saída).')
        if movement_type == 'scrap' and not cleaned_data.get('scrap_reason'):
            self.add_error('scrap_reason', 'Selecione o motivo da sucata.')
        return cleaned_data