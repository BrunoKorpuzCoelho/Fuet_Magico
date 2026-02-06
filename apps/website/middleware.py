from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class LanguageFromURLMiddleware(MiddlewareMixin):
    """
    Middleware to handle language switching via ?lang= parameter.
    Redirects to the appropriate i18n_patterns URL prefix.
    """
    
    def process_request(self, request):
        lang_code = request.GET.get('lang')
        
        if not lang_code:
            return None
        
        supported_languages = ['pt', 'en', 'fr']
        
        if lang_code not in supported_languages:
            return None
        
        # Get the current path
        path = request.path_info
        
        # Remove any existing language prefix
        for lang in supported_languages:
            if path.startswith(f'/{lang}/'):
                path = path[len(f'/{lang}'):]
                break
        
        # Build the new URL with correct language prefix
        if lang_code == 'pt':
            # Portuguese is the default, no prefix needed
            new_path = path
        else:
            # Other languages need prefix
            new_path = f'/{lang_code}{path}'
        
        # Only redirect if the path actually changed
        if new_path == request.path_info:
            return None
        
        # Preserve query params except 'lang'
        query_params = request.GET.copy()
        query_params.pop('lang', None)
        query_string = query_params.urlencode()
        
        new_url = new_path
        if query_string:
            new_url += f'?{query_string}'
        
        response = redirect(new_url, permanent=False)
        response.set_cookie(
            'django_language',
            lang_code,
            max_age=365 * 24 * 60 * 60, 
            path='/',
            samesite='Lax'
        )
        return response
