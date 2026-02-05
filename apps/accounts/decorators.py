from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def login_required_custom(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        return function(request, *args, **kwargs)
    return wrap


def role_required(*roles):
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('accounts:login'))
            
            if request.user.role not in roles:
                return HttpResponseForbidden('Access denied: insufficient permissions')
            
            return function(request, *args, **kwargs)
        return wrap
    return decorator
