"""
Meta WhatsApp Business API — Template submission service.

Docs: https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates
"""
import requests

META_API_VERSION = 'v19.0'


def _get_wa_config(company):
    """
    Fetch the active CompanyWhatsAppConfig for the given company.
    Returns (config, error_message). On success, error_message is None.
    """
    if company is None:
        return None, 'Template sem empresa associada. Edita o template e associa uma empresa.'
    from apps.core.models import CompanyWhatsAppConfig
    try:
        config = CompanyWhatsAppConfig.objects.get(company=company, is_active=True)
    except CompanyWhatsAppConfig.DoesNotExist:
        return None, f'Sem configuração WhatsApp para "{company.name}". Vai a Configurações → WhatsApp.'
    if not config.has_whatsapp_configured:
        return None, f'Configuração WhatsApp incompleta para "{company.name}". Verifica Phone Number ID e Access Token.'
    return config, None


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
        processed = []
        for btn in buttons:
            btn_type = btn.get('type')

            if btn_type == 'URL':
                url = (btn.get('url') or '').strip()
                text = (btn.get('text') or '').strip()
                if not url or not text:
                    continue  # skip incomplete URL buttons — Meta rejects empty url
                b = {'type': 'URL', 'text': text, 'url': url}
                # DYNAMIC buttons require an example value
                if btn.get('example'):
                    b['example'] = btn['example'] if isinstance(btn['example'], list) else [url]
                processed.append(b)

            elif btn_type == 'PHONE_NUMBER':
                text = (btn.get('text') or '').strip()
                raw = str(btn.get('phone_number') or '').strip()
                if not raw or not text:
                    continue  # skip incomplete phone buttons
                # Normalise to E.164
                digits_only = ''.join(c for c in raw if c.isdigit() or c == '+')
                if not digits_only.startswith('+'):
                    digits_only = '+' + digits_only
                processed.append({'type': 'PHONE_NUMBER', 'text': text, 'phone_number': digits_only})

            elif btn_type == 'QUICK_REPLY':
                text = (btn.get('text') or '').strip()
                if text:
                    processed.append({'type': 'QUICK_REPLY', 'text': text})

        if processed:
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

    Credentials are read from CompanyWhatsAppConfig (stored encrypted in DB).

    Returns:
        (success: bool, data: dict)
        On success, data contains the Meta response (includes 'id' and 'status').
        On failure, data contains {'error': 'message'}.
    """
    config, err = _get_wa_config(template.owner_company)
    if err:
        return False, {'error': err}

    access_token = config.get_decrypted_token()
    waba_id = config.business_account_id

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
            err = data.get('error', {})
            if isinstance(err, dict):
                # Prefer the human-readable user message when available
                msg = err.get('error_user_msg') or err.get('error_user_title') or err.get('message', str(data))
            else:
                msg = str(data)
            return False, {'error': msg}

    except requests.RequestException as exc:
        return False, {'error': f'Erro de ligação à Meta: {str(exc)}'}


def delete_template_from_meta(template):
    """
    Delete a message template from Meta.

    Uses DELETE /WABA_ID/message_templates?name={name}
    This removes all language variants with that name.

    Returns:
        (success: bool, error: str | None)
        success=True even if Meta says the template doesn't exist (already gone).
    """
    config, err = _get_wa_config(template.owner_company)
    if err:
        # No WA config — skip Meta call, let DB delete proceed
        return True, None

    access_token = config.get_decrypted_token()
    waba_id = config.business_account_id

    url = f'https://graph.facebook.com/{META_API_VERSION}/{waba_id}/message_templates'
    params = {'name': template.name}

    try:
        response = requests.delete(
            url,
            headers={'Authorization': f'Bearer {access_token}'},
            params=params,
            timeout=15,
        )
        data = response.json()

        # Meta returns {"success": true} on success
        if response.ok and data.get('success'):
            return True, None

        # If template doesn't exist on Meta side, treat as success
        err_code = data.get('error', {}).get('code') if isinstance(data.get('error'), dict) else None
        if err_code in (100, 2388094):  # not found codes
            return True, None

        err_obj = data.get('error', {})
        if isinstance(err_obj, dict):
            msg = err_obj.get('error_user_msg') or err_obj.get('message', str(data))
        else:
            msg = str(data)
        return False, msg

    except requests.RequestException as exc:
        return False, f'Erro de ligação à Meta: {str(exc)}'


def fetch_all_meta_templates(config):
    """
    Fetch all templates from the Meta API (handles pagination).

    Args:
        config: CompanyWhatsAppConfig instance with valid credentials.

    Returns:
        (success: bool, templates: list[dict] | error: dict)
        On success, templates is a list of dicts with at least 'name' and 'status'.
    """
    access_token = config.get_decrypted_token()
    waba_id = config.business_account_id

    url = f'https://graph.facebook.com/{META_API_VERSION}/{waba_id}/message_templates'
    params = {'fields': 'name,status,category,language', 'limit': 200}
    all_templates = []

    try:
        while url:
            response = requests.get(
                url,
                headers={'Authorization': f'Bearer {access_token}'},
                params=params,
                timeout=15,
            )
            data = response.json()

            if not response.ok:
                err = data.get('error', {})
                msg = err.get('message', str(data)) if isinstance(err, dict) else str(data)
                return False, {'error': msg}

            all_templates.extend(data.get('data', []))

            # Follow pagination cursor
            paging = data.get('paging', {})
            url = paging.get('next')  # None if last page
            params = {}  # 'next' already contains params

        return True, all_templates

    except requests.RequestException as exc:
        return False, {'error': f'Erro de ligação à Meta: {str(exc)}'}


def sync_pending_templates():
    """
    Query Meta API for all templates and update the status of any local
    template that is currently PENDING.

    Iterates over all companies that have pending templates — each company
    uses its own CompanyWhatsAppConfig credentials.

    Returns:
        (success: bool, results: list[dict] | error: dict)

        Each result dict:
            {
                'name': str,
                'display_name': str,
                'old_status': str,
                'new_status': str,
                'changed': bool,
                'note': str,
            }
    """
    from apps.whatsapp.models import WhatsAppTemplate  # avoid circular import

    pending_qs = (
        WhatsAppTemplate.objects
        .filter(status=WhatsAppTemplate.STATUS_PENDING)
        .select_related('owner_company')
    )
    pending_templates = list(pending_qs)

    if not pending_templates:
        return True, []

    # Group templates by company to minimise Meta API calls (1 per company)
    company_map: dict = {}
    for template in pending_templates:
        company_map.setdefault(template.owner_company, []).append(template)

    all_results = []

    for company, templates in company_map.items():
        config, err = _get_wa_config(company)
        if err:
            for template in templates:
                all_results.append({
                    'name': template.name,
                    'display_name': template.display_name,
                    'old_status': template.status,
                    'new_status': template.status,
                    'changed': False,
                    'note': err,
                })
            continue

        success, data = fetch_all_meta_templates(config)
        if not success:
            error_msg = data.get('error', 'Erro ao contactar Meta') if isinstance(data, dict) else str(data)
            for template in templates:
                all_results.append({
                    'name': template.name,
                    'display_name': template.display_name,
                    'old_status': template.status,
                    'new_status': template.status,
                    'changed': False,
                    'note': error_msg,
                })
            continue

        # Build lookup: template_name -> status
        meta_status_map = {t['name']: t['status'] for t in data}

        for template in templates:
            meta_status = meta_status_map.get(template.name)

            if meta_status is None:
                all_results.append({
                    'name': template.name,
                    'display_name': template.display_name,
                    'old_status': template.status,
                    'new_status': template.status,
                    'changed': False,
                    'note': 'Não encontrado na Meta',
                })
                continue

            old_status = template.status
            changed = (meta_status != old_status)

            if changed:
                template.status = meta_status
                template.save(update_fields=['status', 'updated_at'])

                # Audit log for status change from Meta sync
                from apps.core.models import AuditLog
                AuditLog.objects.create(
                    user=None,
                    action='UPDATE',
                    model_name='WhatsAppTemplate',
                    object_id=str(template.pk),
                    details={
                        'display_name': template.display_name,
                        'changes': {
                            'status': {
                                'old': old_status,
                                'new': meta_status,
                            },
                        },
                        'note': 'Sincronização automática com Meta API',
                    },
                )

            all_results.append({
                'name': template.name,
                'display_name': template.display_name,
                'old_status': old_status,
                'new_status': meta_status,
                'changed': changed,
                'note': '',
            })

    return True, all_results
