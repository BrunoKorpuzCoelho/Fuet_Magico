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


# ---------------------------------------------------------------------------
# App-level role helpers
# ---------------------------------------------------------------------------

def get_app_role(user, app, company_id):
    """
    Devolve o level ('readonly','user','manager','admin') do utilizador
    para uma aplicação+empresa, ou None se não tiver acesso.
    """
    from .models import AppRole
    try:
        return AppRole.objects.get(user=user, app=app, company_id=company_id).level
    except AppRole.DoesNotExist:
        return None


def has_app_access(user, app, company_id, min_level='user'):
    """True se o utilizador tiver pelo menos min_level para esta app+empresa."""
    LEVELS = {'readonly': 0, 'user': 1, 'manager': 2, 'admin': 3}
    level = get_app_role(user, app, company_id)
    if level is None:
        return False
    return LEVELS.get(level, -1) >= LEVELS.get(min_level, 0)


def require_app_role(app, min_level='user'):
    """
    Decorator que garante que o utilizador tem pelo menos min_level
    para a app especificada na empresa ativa da sessão.

    Uso::

        @login_required
        @require_app_role('crm', min_level='manager')
        def crm_settings(request):
            ...
    """
    LEVELS = {'readonly': 0, 'user': 1, 'manager': 2, 'admin': 3}

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('accounts:login'))
            company_id = request.session.get('active_company_id')
            if not company_id:
                raise PermissionDenied
            level = get_app_role(request.user, app, company_id)
            if level is None or LEVELS.get(level, -1) < LEVELS.get(min_level, 0):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
