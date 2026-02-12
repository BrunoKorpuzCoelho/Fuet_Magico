from django import forms
from datetime import date
from .models import CRMStage, Lead, Activity


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


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'contact', 'title', 'description', 'estimated_value', 
            'probability', 'priority', 'stage', 'source', 
            'expected_close_date', 'assigned_to', 'lost_reason', 'tags'
        ]
        widgets = {
            'contact': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
                'required': True,
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'placeholder': 'Ex: Bolo de Aniversário Premium',
                'maxlength': '255',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'placeholder': 'Descrição detalhada da oportunidade...',
                'rows': '4',
            }),
            'estimated_value': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00',
            }),
            'probability': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'min': '0',
                'max': '100',
                'placeholder': '10',
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
            }),
            'stage': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
                'required': True,
            }),
            'source': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
            }),
            'expected_close_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
            }),
            'lost_reason': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'placeholder': 'Motivo da perda (obrigatório se Lost)...',
                'rows': '3',
            }),
            'tags': forms.HiddenInput(),
        }
        labels = {
            'contact': 'Contacto',
            'title': 'Título da Oportunidade',
            'description': 'Descrição',
            'estimated_value': 'Valor Estimado (Expected Revenue)',
            'probability': 'Probabilidade (%)',
            'priority': 'Prioridade',
            'stage': 'Estágio',
            'source': 'Origem',
            'expected_close_date': 'Data Prevista de Fecho',
            'assigned_to': 'Responsável',
            'lost_reason': 'Motivo da Perda',
            'tags': 'Etiquetas',
        }
        help_texts = {
            'contact': 'Selecione o contacto associado a esta oportunidade.',
            'title': 'Título descritivo da oportunidade de venda.',
            'estimated_value': 'Valor estimado da receita esperada.',
            'probability': 'Probabilidade de fecho entre 0 e 100%.',
            'priority': 'Nível de prioridade (LOW=★, MEDIUM=★★, HIGH=★★★).',
            'stage': 'Estágio atual no pipeline.',
            'lost_reason': 'Obrigatório se o estágio for marcado como perdido.',
        }
    
    def clean_estimated_value(self):
        value = self.cleaned_data.get('estimated_value')
        if value and value < 0:
            raise forms.ValidationError('Valor estimado deve ser maior ou igual a zero.')
        return value
    
    def clean_probability(self):
        probability = self.cleaned_data.get('probability')
        if probability is not None and (probability < 0 or probability > 100):
            raise forms.ValidationError('Probabilidade deve estar entre 0 e 100%.')
        return probability
    
    def clean(self):
        cleaned_data = super().clean()
        stage = cleaned_data.get('stage')
        lost_reason = cleaned_data.get('lost_reason')
        
        if stage and stage.name and 'lost' in stage.name.lower():
            if not lost_reason or len(lost_reason.strip()) < 10:
                raise forms.ValidationError({
                    'lost_reason': 'Motivo da perda é obrigatório e deve ter pelo menos 10 caracteres quando o estágio é "Lost".'
                })
        
        return cleaned_data


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['lead', 'activity_type', 'summary', 'due_date', 'assigned_to', 'is_done', 'feedback']
        widgets = {
            'lead': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
                'required': True,
            }),
            'activity_type': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
                'required': True,
            }),
            'summary': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'placeholder': 'Ex: Follow-up call to discuss pricing',
                'maxlength': '255',
                'required': True,
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
                'required': True,
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 focus:border-primary focus:ring-primary',
            }),
            'is_done': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 bg-gray-700 border-gray-600 rounded focus:ring-green-500 focus:ring-2',
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-700 bg-gray-800 px-4 py-3 text-sm text-gray-300 placeholder-gray-500 focus:border-primary focus:ring-primary',
                'placeholder': 'Feedback ao marcar como concluída (obrigatório)...',
                'rows': '3',
            }),
        }
        labels = {
            'lead': 'Lead/Oportunidade',
            'activity_type': 'Tipo de Atividade',
            'summary': 'Resumo',
            'due_date': 'Data Limite',
            'assigned_to': 'Responsável',
            'is_done': 'Concluído',
            'feedback': 'Feedback',
        }
        help_texts = {
            'lead': 'Lead associada a esta atividade.',
            'activity_type': 'Tipo de atividade (Call, Email, Meeting, etc.).',
            'summary': 'Título descritivo da atividade.',
            'due_date': 'Data limite para conclusão da atividade.',
            'assigned_to': 'Pessoa responsável pela atividade.',
            'is_done': 'Marque quando a atividade estiver concluída.',
            'feedback': 'Obrigatório ao marcar como concluída.',
        }
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        
        if self.instance and self.instance.pk:
            return due_date
        
        if due_date and due_date < date.today():
            raise forms.ValidationError('Data limite não pode ser no passado.')
        
        return due_date
    
    def clean(self):
        cleaned_data = super().clean()
        is_done = cleaned_data.get('is_done')
        feedback = cleaned_data.get('feedback')
        
        if is_done and (not feedback or len(feedback.strip()) < 10):
            raise forms.ValidationError({
                'feedback': 'Feedback é obrigatório e deve ter pelo menos 10 caracteres ao marcar como concluída.'
            })
        
        return cleaned_data
