"""
Forms for Activities System.

This module contains forms for creating, editing, and completing scheduled activities.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import ActivityType, ScheduledActivity, ActivityLog

User = get_user_model()


class ScheduledActivityForm(forms.ModelForm):
    """
    Form for creating and editing scheduled activity blueprints.

    A blueprint defines WHAT the activity is (type, name, summary, description, icon).
    Scheduling (due_date, assigned_to) happens in ActivityLog when the chain runs.
    """

    APPLICABLE_MODEL_CHOICES = [
        ('CRM', 'CRM — Leads'),
        ('WHATSAPP', 'WhatsApp Templates'),
        ('CONTACT', 'Contactos'),
    ]

    applicable_models = forms.MultipleChoiceField(
        choices=APPLICABLE_MODEL_CHOICES,
        required=False,
        label='Modelos aplicáveis',
        help_text='Deixar vazio para aplicar a todos os módulos.',
    )

    class Meta:
        model = ScheduledActivity
        fields = [
            'activity_type',
            'name',
            'summary',
            'description',
            'icon_svg',
            'icon_color',
        ]
        widgets = {
            'activity_type': forms.Select(attrs={
                'class': 'w-full border-0 border-b border-transparent bg-gray-800 text-sm text-gray-300 focus:border-primary focus:ring-0 focus:outline-none py-1 hover:border-gray-600 cursor-pointer',
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full border-0 border-b-2 border-gray-600 bg-transparent text-3xl font-light text-gray-300 placeholder-gray-600 focus:border-primary focus:ring-0 focus:outline-none py-2 px-1',
                'placeholder': 'ex: Ligar ao cliente para follow-up...',
            }),
            'summary': forms.TextInput(attrs={
                'class': 'w-full border-0 border-b border-transparent bg-transparent text-sm text-gray-300 placeholder-gray-600 focus:border-primary focus:ring-0 focus:outline-none py-1 hover:border-gray-600',
                'placeholder': 'Breve descrição do que deve ser feito...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border-0 border-b border-transparent bg-transparent text-sm text-gray-300 placeholder-gray-600 focus:border-primary focus:ring-0 focus:outline-none py-1 hover:border-gray-600 resize-none',
                'rows': 4,
                'placeholder': 'Instruções detalhadas para quem executa esta atividade...',
            }),
            'icon_svg': forms.Textarea(attrs={
                'class': 'w-full border-0 bg-gray-900 text-gray-300 placeholder-gray-600 focus:ring-0 focus:outline-none font-mono text-xs rounded-lg p-3 resize-none',
                'rows': 7,
                'placeholder': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">\n  ...\n</svg>',
                'id': 'id_icon_svg',
            }),
            'icon_color': forms.HiddenInput(attrs={
                'id': 'id_icon_color',
            }),
        }
        labels = {
            'activity_type': 'Tipo de Atividade',
            'name': 'Nome',
            'summary': 'Sumário',
            'description': 'Descrição',
            'icon_svg': 'Ícone SVG',
            'icon_color': 'Cor do Ícone',
        }

    def __init__(self, *args, **kwargs):
        kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        # Queryset do tipo: só tipos ativos, ordenados por nome
        self.fields['activity_type'].queryset = ActivityType.objects.filter(is_active=True).order_by('name')
        self.fields['activity_type'].empty_label = '---------'
        self.fields['name'].required = True
        self.fields['activity_type'].required = True
        self.fields['summary'].required = False
        self.fields['icon_svg'].required = False
        self.fields['icon_color'].required = False
        # Set initial value for applicable_models from instance
        if self.instance and self.instance.pk:
            self.initial['applicable_models'] = self.instance.applicable_models or []

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.applicable_models = self.cleaned_data.get('applicable_models', [])
        if commit:
            instance.save()
        return instance


class ActivityLogForm(forms.ModelForm):
    """
    Form for logging the result of a chain step execution.
    
    Used when a user completes a step in an ActivityChainInstance:
    - Records what happened (result)
    - Captures detailed notes
    - Optionally sets due_date/time for this specific step instance
    
    Previously called ActivityMarkDoneForm (for ScheduledActivity.is_done).
    Now logs into ActivityLog instead.
    """
    
    class Meta:
        model = ActivityLog
        fields = ['result', 'notes', 'due_date', 'due_time', 'assigned_to']
        widgets = {
            'result': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'data-result-selector': 'true',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': _('Describe what happened in this activity...'),
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'due_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time',
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'result': _('Result'),
            'notes': _('Notes'),
            'due_date': _('Due Date'),
            'due_time': _('Due Time'),
            'assigned_to': _('Assigned To'),
        }
        help_texts = {
            'result': _('How did this activity go?'),
            'notes': _('Provide details about what happened'),
        }
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        
        self.fields['result'].required = True
        
        # Filter assigned_to by company if provided
        if company:
            self.fields['assigned_to'].queryset = User.objects.filter(
                owner_company=company,
                is_active=True
            ).order_by('first_name', 'last_name')
        else:
            self.fields['assigned_to'].queryset = User.objects.filter(
                is_active=True
            ).order_by('first_name', 'last_name')
    
    def save(self, commit=True):
        """Override save to auto-set is_done and done_at when result is provided."""
        instance = super().save(commit=False)
        
        if instance.result:
            instance.is_done = True
            if not instance.done_at:
                from django.utils import timezone
                instance.done_at = timezone.now()
        
        if commit:
            instance.save()
        
        return instance


# Backwards-compatible alias
ActivityMarkDoneForm = ActivityLogForm


class ActivityQuickCreateForm(forms.Form):
    """
    Quick form for creating activity from template.
    
    Used in:
    - Quick create buttons
    - Template-based activity creation
    - Workflow suggestions modal
    
    Takes template_id and optional overrides (due_date, assigned_to).
    """
    
    template = forms.ModelChoiceField(
        queryset=ScheduledActivity.objects.filter(is_active=True),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label=_('Activity Blueprint'),
        help_text=_('Escolha o blueprint de atividade'),
    )
    
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
        }),
        label=_('Due Date'),
        help_text=_('Override template default due date'),
    )
    
    due_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'class': 'form-input',
            'type': 'time',
        }),
        label=_('Due Time'),
        help_text=_('Optional: specific time'),
    )
    
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label=_('Assigned To'),
        help_text=_('Override template default assigned user'),
    )
    
    summary_override = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Optional: customize summary'),
        }),
        label=_('Custom Summary'),
        help_text=_('Leave empty to use template default'),
    )
    
    description_override = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 2,
            'placeholder': _('Optional: add additional notes'),
        }),
        label=_('Additional Notes'),
        help_text=_('Appended to template description'),
    )
    
    def __init__(self, *args, **kwargs):
        """
        Initialize with optional filters.
        
        Kwargs:
        - company: Filter templates and users by company
        - activity_type: Pre-filter templates by type
        """
        company = kwargs.pop('company', None)
        activity_type = kwargs.pop('activity_type', None)
        
        super().__init__(*args, **kwargs)
        
        # Filter templates
        blueprint_qs = ScheduledActivity.objects.filter(is_active=True)

        if company:
            blueprint_qs = blueprint_qs.filter(owner_company=company)

        if activity_type:
            blueprint_qs = blueprint_qs.filter(activity_type=activity_type)

        self.fields['template'].queryset = blueprint_qs.order_by('activity_type', 'name', 'summary')
        
        # Filter users
        if company:
            self.fields['assigned_to'].queryset = User.objects.filter(
                owner_company=company,
                is_active=True
            ).order_by('first_name', 'last_name')
    
    def create_activity(self, content_object=None, user=None, company=None):
        """
        Retorna o blueprint selecionado, criando uma cópia se houver overrides.

        Na nova arquitectura, o blueprint (ScheduledActivity) é imutável e reutilizável.
        Se summary_override ou description_override forem fornecidos, cria um novo blueprint derivado.

        Returns:
            ScheduledActivity instance
        """
        blueprint = self.cleaned_data['template']  # já é um ScheduledActivity

        summary_override = self.cleaned_data.get('summary_override')
        description_override = self.cleaned_data.get('description_override')

        if summary_override or description_override:
            new_description = blueprint.description
            if description_override:
                new_description = (blueprint.description + '\n\n' + description_override) if blueprint.description else description_override

            activity = ScheduledActivity.objects.create(
                activity_type=blueprint.activity_type,
                name=blueprint.name,
                summary=summary_override or blueprint.summary,
                description=new_description,
                icon=blueprint.icon,
                icon_svg=blueprint.icon_svg,
                icon_color=blueprint.icon_color,
                decoration_type=blueprint.decoration_type,
                owner_company=company or blueprint.owner_company,
            )
            return activity

        return blueprint
