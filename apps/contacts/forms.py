from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'contact_category',
            'contact_type',
            'name',
            'email',
            'phone',
            'whatsapp',
            'nif',
            'address',
            'city',
            'district',
            'postal_code',
            'country',
            'website',
            'language',
            'company',
            'position',
            'notes',
        ]
        widgets = {
            'contact_category': forms.RadioSelect(attrs={'class': 'contact-category-radio'}),
            'contact_type': forms.RadioSelect(attrs={'class': 'contact-type-radio'}),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: João Silva',
                'maxlength': '255',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'exemplo@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+351 912 345 678',
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+351 912 345 678',
            }),
            'nif': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '123456789',
                'maxlength': '20',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Rua, número, andar...',
                'rows': 2,
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '1000-001',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Lisboa',
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Lisboa, Porto...',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Portugal',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://www.exemplo.pt',
            }),
            'language': forms.Select(attrs={
                'class': 'form-select',
            }),
            'company': forms.Select(attrs={
                'class': 'form-select',
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Gerente, Desenvolvedor...',
                'maxlength': '100',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Informações adicionais...',
                'rows': 4,
            }),
        }
        labels = {
            'contact_category': 'Categoria',
            'contact_type': 'Tipo',
            'name': 'Nome Completo / Empresa',
            'email': 'Email',
            'phone': 'Telefone',
            'whatsapp': 'WhatsApp',
            'nif': 'NIF / Tax ID',
            'address': 'Morada',
            'postal_code': 'Código Postal',
            'city': 'Cidade',
            'district': 'Distrito',
            'country': 'País',
            'website': 'Website',
            'language': 'Idioma',
            'company': 'Empresa',
            'position': 'Cargo / Posição',
            'notes': 'Notas',
        }

