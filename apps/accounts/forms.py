from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from apps.core.models import Company


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-[#dbc693] focus:ring-2 focus:ring-[#dbc693] focus:outline-none transition',
            'placeholder': 'seu@email.com'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-[#dbc693] focus:ring-2 focus:ring-[#dbc693] focus:outline-none transition',
            'placeholder': '••••••••'
        })
    )

# ─── shared widget classes ────────────────────────────────────────────────────
_INPUT  = 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition text-sm'
_SELECT = 'w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition text-sm'


class UserCreateForm(forms.ModelForm):
    """Formulário para criar um novo utilizador (usado por ADMIN)."""

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT, 'placeholder': '••••••••'}),
    )
    password2 = forms.CharField(
        label='Confirmar Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT, 'placeholder': '••••••••'}),
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'role',
                  'companies', 'default_company', 'phone', 'is_active']
        widgets = {
            'first_name':       forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Nome'}),
            'last_name':        forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Apelido'}),
            'username':         forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'utilizador'}),
            'email':            forms.EmailInput(attrs={'class': _INPUT, 'placeholder': 'email@exemplo.com'}),
            'phone':            forms.TextInput(attrs={'class': _INPUT, 'placeholder': '+351 900 000 000'}),
            'role':             forms.Select(attrs={'class': _SELECT}),
            'companies':        forms.CheckboxSelectMultiple(),
            'default_company':  forms.Select(attrs={'class': _SELECT}),
            'is_active':        forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-600 bg-gray-700 text-primary focus:ring-primary'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1', '')
        p2 = self.cleaned_data.get('password2', '')
        if p1 != p2:
            raise ValidationError('As passwords não coincidem.')
        if len(p1) < 8:
            raise ValidationError('A password deve ter pelo menos 8 caracteres.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserEditForm(forms.ModelForm):
    """Formulário para editar um utilizador existente (usado por ADMIN)."""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone',
                  'role', 'companies', 'default_company', 'is_active']
        widgets = {
            'first_name':       forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Primeiro nome'}),
            'last_name':        forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Apelido'}),
            'username':         forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'nome_utilizador'}),
            'email':            forms.EmailInput(attrs={'class': _INPUT, 'placeholder': 'email@exemplo.com'}),
            'phone':            forms.TextInput(attrs={'class': _INPUT, 'placeholder': '+351 900 000 000'}),
            'role':             forms.Select(attrs={'class': _SELECT}),
            'companies':        forms.CheckboxSelectMultiple(),
            'default_company':  forms.Select(attrs={'class': _SELECT}),
            'is_active':        forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-600 bg-gray-700 text-primary focus:ring-primary'}),
        }


class SetNewPasswordForm(forms.Form):
    """Formulário de definir nova password via token de reset."""

    new_password1 = forms.CharField(
        label='Nova Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT, 'placeholder': '••••••••', 'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label='Confirmar Nova Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT, 'placeholder': '••••••••', 'autocomplete': 'new-password'}),
    )

    def clean_new_password2(self):
        p1 = self.cleaned_data.get('new_password1', '')
        p2 = self.cleaned_data.get('new_password2', '')
        if p1 != p2:
            raise ValidationError('As passwords não coincidem.')
        if len(p1) < 8:
            raise ValidationError('A password deve ter pelo menos 8 caracteres.')
        return p2