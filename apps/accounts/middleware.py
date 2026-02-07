from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden


class AuthenticationMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = ['/dashboard/', '/contacts/']
        self.public_paths = ['/login/', '/logout/', '/admin/', '/i18n/']
    
    def __call__(self, request):
        path = request.path
        
        is_protected = any(path.startswith(protected) for protected in self.protected_paths)
        is_public = any(path.startswith(public) for public in self.public_paths)
        
        if is_protected and not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        
        response = self.get_response(request)
        return response
