from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def login_required_custom(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        return function(request, *args, **kwargs)
    return wrap


def role_required(*roles):
    """
    Decorator that checks if user has one of the allowed roles.
    Usage:
        @role_required('ADMIN', 'MANAGER')
        def my_view(request):
            pass
    """
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('accounts:login'))
            
            if request.user.role not in roles:
                roles_str = ', '.join(roles)
                messages.error(request, f'Acesso negado. Roles permitidas: {roles_str}')
                return HttpResponseForbidden(f'Access denied: Role must be one of {roles_str}')
            
            return function(request, *args, **kwargs)
        return wrap
    return decorator


def admin_required(function):
    """
    Decorator to restrict access to ADMIN role only.
    Usage:
        @admin_required
        def delete_user(request, user_id):
            # Only ADMIN can access
            pass
    """
    return role_required('ADMIN')(function)


def manager_or_admin_required(function):
    """
    Decorator for MANAGER and ADMIN access.
    Usage:
        @manager_or_admin_required
        def edit_contact(request, contact_id):
            # MANAGER and ADMIN can access
            pass
    """
    return role_required('ADMIN', 'MANAGER')(function)


def staff_required(function):
    """
    Alias for manager_or_admin_required.
    Staff = MANAGER or ADMIN
    """
    return manager_or_admin_required(function)


# Helper functions for use in views/templates
def is_admin(user):
    """Check if user is ADMIN"""
    return user.is_authenticated and user.role == 'ADMIN'


def is_manager(user):
    """Check if user is MANAGER"""
    return user.is_authenticated and user.role == 'MANAGER'


def is_employee(user):
    """Check if user is EMPLOYEE"""
    return user.is_authenticated and user.role == 'EMPLOYEE'


def is_staff(user):
    """Check if user is MANAGER or ADMIN"""
    return user.is_authenticated and user.role in ['ADMIN', 'MANAGER']


def can_delete(user):
    """Check if user can delete records (ADMIN only)"""
    return is_admin(user)


def can_edit(user):
    """Check if user can edit records (MANAGER and ADMIN)"""
    return is_staff(user)
