"""
Context processors for accounts app.
Makes user companies and active company available in all templates.
"""
from apps.core.models import Company


def company_context(request):
    """
    Add active company and user companies to template context.
    
    Returns:
        dict: Context with 'active_company' and 'user_companies'
    """
    context = {
        'active_company': None,
        'user_companies': []
    }
    
    if request.user.is_authenticated:
        # Get active company from session or use default_company
        active_company_id = request.session.get('active_company_id')
        
        if active_company_id:
            try:
                context['active_company'] = Company.objects.get(id=active_company_id)
            except Company.DoesNotExist:
                # If company in session doesn't exist, use default
                context['active_company'] = request.user.default_company
                if context['active_company']:
                    request.session['active_company_id'] = str(context['active_company'].id)
        else:
            # No company in session, use default
            context['active_company'] = request.user.default_company
            if context['active_company']:
                request.session['active_company_id'] = str(context['active_company'].id)
        
        # Get all companies user has access to
        if request.user.is_superuser:
            context['user_companies'] = Company.objects.filter(is_active=True).order_by('name')
        else:
            context['user_companies'] = request.user.companies.filter(is_active=True).order_by('name')
    
    return context
