"""
Meta WhatsApp Business API — Template submission service.

Docs: https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates
"""
import requests
from django.conf import settings

META_API_VERSION = 'v19.0'


def build_template_payload(template):
    """
    Build the JSON payload expected by the Meta API for template creation.
    """
    components = []

    # ---- HEADER ----
    if template.header_type != 'NONE':
        header = {'type': 'HEADER', 'format': template.header_type}
        if template.header_type == 'TEXT' and template.header_text:
            header['text'] = template.header_text
            # If header contains {{1}}, include example
            if '{{1}}' in template.header_text:
                header['example'] = {'header_text': ['exemplo_cabecalho']}
        components.append(header)

    # ---- BODY ----
    body_component = {'type': 'BODY', 'text': template.body}

    # Collect variable samples in order for the example
    if template.variables:
        keys = sorted(template.variables.keys(), key=lambda k: int(k))
        samples = []
        for k in keys:
            v = template.variables[k]
            sample = v.get('sample', '') if isinstance(v, dict) else str(v)
            samples.append(sample or f'variavel_{k}')
        if samples:
            body_component['example'] = {'body_text': [samples]}

    components.append(body_component)

    # ---- FOOTER ----
    if template.footer:
        components.append({'type': 'FOOTER', 'text': template.footer})

    # ---- BUTTONS ----
    if template.buttons:
        buttons = template.buttons if isinstance(template.buttons, list) else []
        if buttons:
            # For DYNAMIC URL buttons, include example
            processed = []
            for btn in buttons:
                b = dict(btn)
                if b.get('type') == 'URL' and b.get('example'):
                    # already has example from our form
                    pass
                processed.append(b)
            components.append({'type': 'BUTTONS', 'buttons': processed})

    return {
        'name': template.name,
        'category': template.category,
        'language': template.language,
        'allow_category_change': template.allow_category_change,
        'components': components,
    }


def submit_template_to_meta(template):
    """
    Submit a WhatsApp template to Meta for approval.

    Returns:
        (success: bool, data: dict)
        On success, data contains the Meta response (includes 'id' and 'status').
        On failure, data contains {'error': 'message'}.
    """
    access_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')
    waba_id = getattr(settings, 'WHATSAPP_WABA_ID', '')

    if not access_token or not waba_id:
        return False, {
            'error': 'WHATSAPP_ACCESS_TOKEN ou WHATSAPP_WABA_ID não configurados. '
                     'Adiciona-os no ficheiro .env e em Configuração → Credenciais API.'
        }

    url = f'https://graph.facebook.com/{META_API_VERSION}/{waba_id}/message_templates'
    payload = build_template_payload(template)

    try:
        response = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=15,
        )
        data = response.json()

        if response.ok and 'id' in data:
            return True, data
        else:
            # Extract Meta's error message
            err = data.get('error', {})
            if isinstance(err, dict):
                msg = err.get('message', str(data))
            else:
                msg = str(data)
            return False, {'error': msg}

    except requests.RequestException as exc:
        return False, {'error': f'Erro de ligação à Meta: {str(exc)}'}
