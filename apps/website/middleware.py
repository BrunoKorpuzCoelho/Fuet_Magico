"""
Middleware para processar parâmetro lang da URL
"""
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageFromURLMiddleware(MiddlewareMixin):
    """
    Middleware que processa o parâmetro ?lang= da URL e ativa o idioma correspondente.
    Também salva a preferência no cookie Django.
    """
    
    def process_request(self, request):
        # Obter parâmetro lang da URL
        lang_code = request.GET.get('lang')
        
        # Lista de idiomas suportados
        supported_languages = ['pt', 'en', 'fr']
        
        if lang_code and lang_code in supported_languages:
            # Ativar o idioma
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code
            
            # Salvar no cookie para persistência
            response = None
            if hasattr(request, '_cached_response'):
                response = request._cached_response
            
        else:
            # Tentar obter do cookie
            lang_code = request.COOKIES.get('django_language')
            if lang_code and lang_code in supported_languages:
                translation.activate(lang_code)
                request.LANGUAGE_CODE = lang_code
    
    def process_response(self, request, response):
        # Se há um lang na URL, salvar no cookie
        lang_code = request.GET.get('lang')
        supported_languages = ['pt', 'en', 'fr']
        
        if lang_code and lang_code in supported_languages:
            response.set_cookie(
                'django_language',
                lang_code,
                max_age=365 * 24 * 60 * 60,  # 1 ano
                path='/',
                samesite='Lax'
            )
        
        return response
