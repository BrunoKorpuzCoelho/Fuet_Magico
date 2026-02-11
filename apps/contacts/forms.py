from django import forms
from .models import Contact, ContactTag


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'contact_category',
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


class ContactTagForm(forms.ModelForm):
    """Formulário para criação e edição de Tags de Contacto"""
    
    class Meta:
        model = ContactTag
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'placeholder': 'Ex: Cliente VIP, Fornecedor Preferencial, Leads...',
                'maxlength': '50',
                'required': True,
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'h-12 w-full rounded-lg border-gray-700 bg-gray-800 cursor-pointer',
                'required': True,
            }),
        }
        labels = {
            'name': 'Nome da Tag',
            'color': 'Cor',
        }
        help_texts = {
            'name': 'Escolha um nome único e descritivo para identificar esta tag.',
            'color': 'Selecione uma cor para destacar esta tag visualmente.',
        }
    
    def clean_name(self):
        """Validar nome único (case-insensitive)"""
        name = self.cleaned_data.get('name')
        
        # Check if updating existing tag
        if self.instance and self.instance.pk:
            # Exclude current instance from uniqueness check
            if ContactTag.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Já existe uma tag com este nome.')
        else:
            # Creating new tag
            if ContactTag.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError('Já existe uma tag com este nome.')
        
        return name
    
    def clean_color(self):
        """Validar formato de cor hexadecimal"""
        color = self.cleaned_data.get('color')
        
        # Ensure it starts with #
        if not color.startswith('#'):
            color = '#' + color
        
        # Validate hex format
        if len(color) != 7:
            raise forms.ValidationError('Cor deve estar no formato #RRGGBB')
        
        try:
            int(color[1:], 16)
        except ValueError:
            raise forms.ValidationError('Cor inválida. Use formato hexadecimal (#RRGGBB)')
        
        return color
