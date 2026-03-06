from django.shortcuts import render


def home(request):
    """
    View para a página inicial do website.
    """
    return render(request, 'website/home.html')


def terms(request):
    """Página pública de Termos e Condições."""
    return render(request, 'website/terms.html')
