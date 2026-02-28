# -*- coding: utf-8 -*-
"""
Compilador Central de Templates de Email.

Responsável por resolver variáveis (placeholders) nos templates de email
antes do envio. Suporta dois formatos de variáveis:

  - Variável curta (numérica):  {{1}}, {{2}}, {{3}} — sem espaços
  - Variável completa (path):   {{ lead.title }}, {{ contact.name }} — com espaços

Cada variável está mapeada no campo `available_placeholders` do EmailTemplate:

    {
        "1": {"field": "lead.contact.name",  "fallback": "Cliente"},
        "2": {"field": "lead.title",         "fallback": "a sua oportunidade"},
    }

O compilador recebe um record (Lead, Contact, etc.) e resolve cada variável
navegando pelas relações do modelo Django (dot notation).

Uso:
    from apps.core.template_compiler import compile_email_template

    result = compile_email_template(template, record=lead, user=request.user)
    # result['subject']   → Assunto com variáveis substituídas
    # result['body_html'] → Body HTML com variáveis substituídas

A função é genérica e pode ser usada por qualquer módulo (CRM, Vendas,
Contactos, Marketing, etc.).
"""

import re
import logging

logger = logging.getLogger(__name__)


# ── Regex patterns ──────────────────────────────────────────────────────────

# {{1}}, {{2}} — sem espaços (variável curta)
_RE_SHORT_VAR = re.compile(r'\{\{(\d+)\}\}')

# {{ lead.title }}, {{ contact.name }} — com espaços (variável completa)
_RE_FULL_VAR = re.compile(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}')


# ── Core: resolver um campo via dot notation ────────────────────────────────

def _resolve_field(obj, field_path: str):
    """
    Resolve um campo via dot notation a partir de um objeto Django.

    Exemplos:
        _resolve_field(lead, 'title')               → lead.title
        _resolve_field(lead, 'contact.name')         → lead.contact.name
        _resolve_field(lead, 'assigned_to.email')    → lead.assigned_to.email
        _resolve_field(lead, 'stage.name')           → lead.stage.name

    Retorna None se o caminho não puder ser resolvido (FK nulo, atributo
    inexistente, etc.).
    """
    current = obj
    for part in field_path.split('.'):
        if current is None:
            return None
        try:
            current = getattr(current, part, None)
        except Exception:
            return None
    return current


# ── Build variable map from template placeholders ───────────────────────────

def _build_var_map(placeholders: dict, record) -> dict:
    """
    Constrói o mapa de substituição a partir dos placeholders do template.

    Args:
        placeholders: Dict do campo `available_placeholders` do EmailTemplate.
            Ex: {"1": {"field": "lead.contact.name", "fallback": "Cliente"}}
        record: Instância do modelo Django (Lead, Contact, etc.)

    Returns:
        Dict com duas entradas por variável:
            - chave numérica (para {{N}}): valor resolvido ou fallback
            - chave field path (para {{ field.path }}): valor resolvido ou fallback
    """
    var_map = {}

    if not placeholders or not isinstance(placeholders, dict):
        return var_map

    for key, config in placeholders.items():
        if not isinstance(config, dict):
            # Formato legacy: {"contact_name": "Descrição do campo"}
            # Tenta resolver o key como field path
            value = None
            if record:
                # Remove o prefixo do modelo raiz se presente
                value = _resolve_field_with_root(record, key)
            var_map[key] = str(value) if value not in (None, '') else str(config)
            continue

        field_path = config.get('field', '')
        fallback = config.get('fallback', '')

        # Resolver o valor real do campo
        value = None
        if record and field_path:
            value = _resolve_field_with_root(record, field_path)

        # Valor final: real se existir, senão fallback
        final = str(value) if value not in (None, '') else fallback

        # Mapear tanto pelo número quanto pelo field path
        var_map[key] = final  # {{1}}, {{2}}, etc.
        if field_path:
            var_map[field_path] = final  # {{ lead.title }}, etc.

    return var_map


def _resolve_field_with_root(record, field_path: str):
    """
    Resolve um field path considerando o nome do modelo raiz.

    Se field_path começa com o nome do modelo raiz do record (ex: 'lead.title'
    para um Lead), remove esse prefixo antes de resolver.
    Se não (ex: 'title'), resolve diretamente.

    Isto permite que 'lead.title' e 'title' funcionem ambos quando o
    record é um Lead.
    """
    # Nome do modelo raiz em minúsculas
    model_name = record.__class__.__name__.lower()

    # Se o path começa com "lead." e o record é Lead → remover prefixo
    if '.' in field_path:
        root, rest = field_path.split('.', 1)
        if root.lower() == model_name:
            return _resolve_field(record, rest)

    # Tentar resolver diretamente (pode ser 'title' sem prefixo)
    return _resolve_field(record, field_path)


# ── Substituição de variáveis num texto ─────────────────────────────────────

def _substitute_vars(text: str, var_map: dict) -> str:
    """
    Substitui todas as variáveis (curtas e completas) num texto.

    Ordem: primeiro as variáveis curtas {{1}}, depois as completas {{ path }}.
    """
    if not text or not var_map:
        return text or ''

    # 1. Substituir variáveis curtas: {{1}}, {{2}}, etc.
    def _replace_short(match):
        num = match.group(1)
        return var_map.get(num, match.group(0))

    result = _RE_SHORT_VAR.sub(_replace_short, text)

    # 2. Substituir variáveis completas: {{ field.path }}
    def _replace_full(match):
        path = match.group(1)
        return var_map.get(path, match.group(0))

    result = _RE_FULL_VAR.sub(_replace_full, result)

    return result


# ── API pública ─────────────────────────────────────────────────────────────

def compile_email_template(template, record=None, user=None, extra_context=None):
    """
    Compila um EmailTemplate, resolvendo todas as variáveis nos campos
    `subject` e `body_html`.

    Args:
        template:       Instância de EmailTemplate (com available_placeholders, subject, body_html).
        record:         Instância do modelo associado (Lead, Contact, etc.) — opcional.
        user:           Utilizador que envia o email (para variáveis como sender_name) — opcional.
        extra_context:  Dict adicional de variáveis para substituir (ex: {'custom_field': 'valor'}).
                        As chaves são usadas como paths no {{ }} e sobrepõem valores resolvidos.

    Returns:
        dict com:
            'subject':   Assunto compilado (variáveis substituídas).
            'body_html': Body HTML compilado (variáveis substituídas).
            'var_map':   Dict de todas as variáveis resolvidas (útil para debug/preview).

    Exemplo:
        from apps.core.template_compiler import compile_email_template
        from apps.core.models import EmailTemplate

        template = EmailTemplate.objects.get(name='Email de Agradecimento')
        lead = Lead.objects.get(pk=some_id)

        result = compile_email_template(template, record=lead, user=request.user)

        # Usar com send_email_for_record:
        send_email_for_record(
            user=request.user,
            record=lead,
            to_email=lead.email_from,
            subject=result['subject'],
            body=strip_tags(result['body_html']),
            body_html=result['body_html'],
        )
    """
    placeholders = template.available_placeholders or {}

    # Construir mapa de variáveis a partir dos placeholders + record
    var_map = _build_var_map(placeholders, record)

    # Adicionar variáveis do utilizador (se disponível)
    if user:
        user_vars = {
            'sender_name': user.get_full_name() or user.username,
            'sender_email': getattr(user, 'email', ''),
            'sender_first_name': getattr(user, 'first_name', ''),
            'sender_last_name': getattr(user, 'last_name', ''),
        }
        # Só adicionar se não existirem já no var_map (templates têm prioridade)
        for k, v in user_vars.items():
            if k not in var_map:
                var_map[k] = str(v) if v else ''

    # Adicionar contexto extra (sobrepõe tudo)
    if extra_context and isinstance(extra_context, dict):
        var_map.update({k: str(v) for k, v in extra_context.items() if v is not None})

    # Substituir variáveis no subject e body_html
    compiled_subject = _substitute_vars(template.subject, var_map)
    compiled_body = _substitute_vars(template.body_html, var_map)

    return {
        'subject': compiled_subject,
        'body_html': compiled_body,
        'var_map': var_map,
    }


def compile_text(text: str, placeholders: dict, record=None, extra_context=None):
    """
    Compila um texto arbitrário usando o mesmo sistema de variáveis.

    Útil para compilar assuntos, SMS, notificações, etc. sem precisar
    de um EmailTemplate completo.

    Args:
        text:           Texto com variáveis {{1}} ou {{ field.path }}.
        placeholders:   Dict de placeholders (mesmo formato do EmailTemplate).
        record:         Instância do modelo Django (opcional).
        extra_context:  Dict adicional de variáveis (opcional).

    Returns:
        str: Texto com variáveis substituídas.
    """
    var_map = _build_var_map(placeholders, record)

    if extra_context and isinstance(extra_context, dict):
        var_map.update({k: str(v) for k, v in extra_context.items() if v is not None})

    return _substitute_vars(text, var_map)
