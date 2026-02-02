from django.shortcuts import render


def home(request):
    """
    View para a página inicial do website.
    """
    return render(request, 'website/home.html')
