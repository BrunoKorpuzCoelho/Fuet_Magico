from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import translate_url


class LanguageFromURLMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        lang_code = request.GET.get('lang')
        
        supported_languages = ['pt', 'en', 'fr']
        
        if lang_code and lang_code in supported_languages:
            # Activate the language
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code
            
            # Get the current path without language prefix
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
            
            # If the path changed, redirect
            if new_path != request.path_info:
                # Preserve query params except 'lang'
                query_params = request.GET.copy()
                query_params.pop('lang', None)
                query_string = query_params.urlencode()
                
                new_url = new_path
                if query_string:
                    new_url += f'?{query_string}'
                
                response = redirect(new_url)
                response.set_cookie(
                    'django_language',
                    lang_code,
                    max_age=365 * 24 * 60 * 60, 
                    path='/',
                    samesite='Lax'
                )
                return response
            
        else:
            lang_code = request.COOKIES.get('django_language')
            if lang_code and lang_code in supported_languages:
                translation.activate(lang_code)
                request.LANGUAGE_CODE = lang_code
    
    def process_response(self, request, response):
        lang_code = request.GET.get('lang')
        supported_languages = ['pt', 'en', 'fr']
        
        if lang_code and lang_code in supported_languages:
            response.set_cookie(
                'django_language',
                lang_code,
                max_age=365 * 24 * 60 * 60, 
                path='/',
                samesite='Lax'
            )
        
        return response
