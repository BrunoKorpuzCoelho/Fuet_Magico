from django import forms
from django.contrib.auth.forms import AuthenticationForm


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
