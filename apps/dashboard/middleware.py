from django.shortcuts import redirect
from django.urls import resolve


class AdminDebugMiddleware:
    """
    Middleware to restrict debug mode (?debug=true) to ADMIN users only.
    Redirects non-admin users to the same URL without the debug parameter.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if debug parameter is in the URL
        if 'debug' in request.GET and request.GET.get('debug') == 'true':
            # Check if user is authenticated and is not ADMIN
            if request.user.is_authenticated and request.user.role != 'ADMIN':
                # Redirect to the same URL without debug parameter
                path = request.path
                query_params = request.GET.copy()
                query_params.pop('debug', None)
                
                if query_params:
                    query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
                    return redirect(f"{path}?{query_string}")
                else:
                    return redirect(path)
        
        response = self.get_response(request)
        return response
