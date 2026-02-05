from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageFromURLMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        lang_code = request.GET.get('lang')
        
        supported_languages = ['pt', 'en', 'fr']
        
        if lang_code and lang_code in supported_languages:
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code
            
            response = None
            if hasattr(request, '_cached_response'):
                response = request._cached_response
            
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
