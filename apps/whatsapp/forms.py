from django import forms
from .models import WhatsAppTemplate


_INPUT = 'w-full h-9 px-3 rounded-md border border-gray-700 bg-[#111827] text-sm text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary'
_SELECT = _INPUT
_TEXTAREA = 'w-full px-3 py-2 rounded-md border border-gray-700 bg-[#111827] text-sm text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary resize-none font-mono'


class WhatsAppTemplateForm(forms.ModelForm):
    class Meta:
        model = WhatsAppTemplate
        fields = [
            'display_name', 'name', 'category', 'language',
            'header_type', 'header_text', 'body', 'footer',
            'buttons', 'variables', 'model_name',
            'allow_category_change', 'owner_company',
            'wa_template_uid',
        ]
        widgets = {
            # Big name — contacts style (border-bottom only, transparent bg, large)
            'display_name': forms.TextInput(attrs={
                'class': 'flex w-full px-3 py-2 h-14 border-0 border-b-2 border-gray-600 bg-transparent text-3xl font-light text-gray-300 placeholder:text-gray-600 focus:border-primary focus:ring-0 focus:outline-none rounded-none',
                'placeholder': 'Nome do template, ex: Orçamento Aprovado',
            }),
            # Technical name — small mono inline
            'name': forms.TextInput(attrs={
                'class': 'flex-1 h-7 px-2 rounded border border-gray-700 bg-[#111827] text-xs text-gray-400 font-mono focus:outline-none focus:ring-1 focus:ring-primary',
                'placeholder': 'nome_tecnico',
            }),
            'category': forms.Select(attrs={'class': _SELECT}),
            'language': forms.Select(attrs={'class': _SELECT}),
            'header_type': forms.Select(attrs={'class': _SELECT}),
            'header_text': forms.TextInput(attrs={
                'class': _INPUT,
                'placeholder': 'Máx. 60 caracteres',
                'maxlength': '60',
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 rounded-md border border-gray-700 bg-[#111827] text-sm text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary resize-none leading-relaxed',
                'rows': 8,
                'placeholder': 'Olá {{1}}, o seu orçamento {{2}} foi aprovado…',
            }),
            'footer': forms.TextInput(attrs={
                'class': _INPUT,
                'placeholder': 'Ex: Write \'stop\' to stop receiving messages',
                'maxlength': '60',
            }),
            'buttons': forms.Textarea(attrs={
                'class': _TEXTAREA,
                'rows': 8,
                'placeholder': '[{"type": "QUICK_REPLY", "text": "Confirmar"}]',
            }),
            'variables': forms.Textarea(attrs={
                'class': _TEXTAREA,
                'rows': 6,
                'placeholder': '{"1": "contact.name", "2": "deal.title"}',
            }),
            'model_name': forms.Select(attrs={'class': _SELECT}),
            'wa_template_uid': forms.TextInput(attrs={
                'class': _INPUT,
                'placeholder': 'Preenchido automaticamente pela Meta',
            }),
        }
