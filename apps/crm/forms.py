from django import forms
from .models import CRMStage


class CRMStageForm(forms.ModelForm):
    """Formulário para criação e edição de Estágios CRM"""
    
    class Meta:
        model = CRMStage
        fields = ['name', 'sequence', 'color', 'routing_in_days', 'is_won_stage', 'fold_by_default']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'placeholder': 'Ex: Novo, Qualificado, Proposta, Won...',
                'maxlength': '100',
                'required': True,
            }),
            'sequence': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'min': '1',
                'required': True,
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'h-12 w-full rounded-lg border-gray-700 bg-gray-800 cursor-pointer',
                'required': True,
            }),
            'routing_in_days': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'min': '0',
            }),
            'is_won_stage': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 bg-gray-700 border-gray-600 rounded focus:ring-green-500 focus:ring-2',
            }),
            'fold_by_default': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary bg-gray-700 border-gray-600 rounded focus:ring-primary focus:ring-2',
            }),
        }
        labels = {
            'name': 'Nome do Estágio',
            'sequence': 'Sequência',
            'color': 'Cor',
            'routing_in_days': 'Dias de Encaminhamento',
            'is_won_stage': 'Estágio de Vitória',
            'fold_by_default': 'Colapsado por Padrão',
        }
        help_texts = {
            'name': 'Escolha um nome único e descritivo para identificar este estágio.',
            'sequence': 'A ordem em que o estágio aparece no pipeline (menor = primeiro).',
            'color': 'Selecione uma cor para destacar este estágio visualmente.',
            'routing_in_days': 'Número de dias antes do encaminhamento automático (0 = desativado).',
            'is_won_stage': 'Marque se este estágio representa uma venda ganha.',
            'fold_by_default': 'Marque para ocultar este estágio na visualização do pipeline por padrão.',
        }
    
    def clean_name(self):
        """Validar nome único (case-insensitive)"""
        name = self.cleaned_data.get('name')
        
        # Check if updating existing stage
        if self.instance and self.instance.pk:
            # Exclude current instance from uniqueness check
            if CRMStage.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Já existe um estágio com este nome.')
        else:
            # Creating new stage
            if CRMStage.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError('Já existe um estágio com este nome.')
        
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
    
    def clean_is_won_stage(self):
        """Validar que só pode haver um estágio de vitória"""
        is_won = self.cleaned_data.get('is_won_stage')
        
        if is_won:
            # Check if another won stage already exists
            existing_won = CRMStage.objects.filter(is_won_stage=True, is_active=True)
            
            # If editing, exclude current instance
            if self.instance and self.instance.pk:
                existing_won = existing_won.exclude(pk=self.instance.pk)
            
            if existing_won.exists():
                raise forms.ValidationError('Já existe um estágio de vitória. Só pode existir um estágio com "Vitória" ativo por empresa.')
        
        return is_won
