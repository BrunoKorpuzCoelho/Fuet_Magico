"""
Sistema central de envio de email via SMTP por utilizador.

Fluxo:
  1. Utilizador configura credenciais em apps.accounts.models.UserEmailConfig
  2. Qualquer módulo chama send_email_for_record(user, record, ...)
  3. A função envia o email via SMTP e guarda um ChatterMessage (message_type='EMAIL')
     ligado ao registo via GenericForeignKey — aparece no chatter desse registo.

Encriptação:
  A App Password é guardada encriptada com Fernet.
  Chave configurada em settings.FERNET_KEY (variável de ambiente FERNET_KEY no .env).
  Gerar: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.utils import formataddr, make_msgid
from email import encoders

from django.conf import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuração por provedor
# ---------------------------------------------------------------------------

SMTP_PROVIDERS = {
    'gmail': {
        'host': 'smtp.gmail.com',
        'port': 587,
        'label': 'Gmail',
    },
    'outlook': {
        'host': 'smtp.office365.com',
        'port': 587,
        'label': 'Outlook / Microsoft 365',
    },
}

IMAP_PROVIDERS = {
    'gmail': {
        'host': 'imap.gmail.com',
        'port': 993,
    },
    'outlook': {
        'host': 'imap.office365.com',
        'port': 993,
    },
}


# ---------------------------------------------------------------------------
# Encriptação Fernet
# ---------------------------------------------------------------------------

def _get_fernet():
    """Retorna instância Fernet com a chave configurada em settings.FERNET_KEY."""
    from cryptography.fernet import Fernet
    key = getattr(settings, 'FERNET_KEY', '')
    if not key:
        raise ValueError(
            'FERNET_KEY não está configurado. Adiciona ao .env:\n'
            '  FERNET_KEY=<chave>\n'
            'Gera uma com: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"'
        )
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_password(raw_password: str) -> str:
    """Encripta uma app password em texto limpo para armazenamento."""
    return _get_fernet().encrypt(raw_password.encode('utf-8')).decode('utf-8')


def decrypt_password(encrypted_password: str) -> str:
    """Desencripta uma app password armazenada."""
    from cryptography.fernet import InvalidToken
    try:
        return _get_fernet().decrypt(encrypted_password.encode('utf-8')).decode('utf-8')
    except InvalidToken:
        raise ValueError(
            'Falha ao desencriptar a App Password. '
            'A FERNET_KEY pode ter mudado desde que a password foi guardada.'
        )


# ---------------------------------------------------------------------------
# Envio SMTP (baixo nível — interno)
# ---------------------------------------------------------------------------

def _send_via_smtp(config, to_email: str, subject: str, body: str,
                   body_html, to_name: str, sender_name: str, attachments=None,
                   cc: str = '', bcc: str = '',
                   in_reply_to: str = '', references: str = '',
                   inline_images=None):
    """
    Envia o email e devolve (success: bool, error: str, message_id: str).
    Não escreve nada na BD.

    attachments: lista de dicts [{"filename": "...", "content": <bytes>, "mime_type": "image/jpeg"}]
    inline_images: lista de dicts [{"cid": "company_logo", "content": <bytes>, "mime_type": "image/png"}]
    """
    provider = SMTP_PROVIDERS.get(config.provider, SMTP_PROVIDERS['gmail'])
    smtp_host = provider['host']
    smtp_port = provider['port']

    try:
        app_password = decrypt_password(config.app_password)
    except ValueError as e:
        return False, str(e), ''

    msg_id = make_msgid(domain=config.email_address.split('@')[-1])
    inline_images = inline_images or []

    # Estrutura da mensagem
    # Com inline images (CID): mixed → related → alternative + images   (+ attachments)
    # Sem inline images:       mixed → alternative + attachments  (ou alternative simples)
    if attachments or inline_images:
        msg = MIMEMultipart('mixed')

        if inline_images:
            # related wraps alternative + inline images
            related = MIMEMultipart('related')
            alt = MIMEMultipart('alternative')
            alt.attach(MIMEText(body, 'plain', 'utf-8'))
            if body_html:
                alt.attach(MIMEText(body_html, 'html', 'utf-8'))
            related.attach(alt)
            # Attach inline CID images
            for img in inline_images:
                maintype, subtype = img['mime_type'].split('/', 1)
                mime_img = MIMEImage(img['content'], _subtype=subtype)
                mime_img.add_header('Content-ID', f'<{img["cid"]}>')
                mime_img.add_header('Content-Disposition', 'inline', filename=f'{img["cid"]}.{subtype}')
                related.attach(mime_img)
            msg.attach(related)
        else:
            alt = MIMEMultipart('alternative')
            alt.attach(MIMEText(body, 'plain', 'utf-8'))
            if body_html:
                alt.attach(MIMEText(body_html, 'html', 'utf-8'))
            msg.attach(alt)

        # Ficheiros anexos normais
        for att in (attachments or []):
            part = MIMEBase(*att['mime_type'].split('/', 1))
            part.set_payload(att['content'])
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=att['filename'])
            msg.attach(part)
    elif body_html:
        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        msg.attach(MIMEText(body_html, 'html', 'utf-8'))
    else:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

    msg['From'] = formataddr((sender_name, config.email_address))

    # Support comma-separated primary recipients in to_email
    to_addresses = [a.strip() for a in to_email.split(',') if a.strip()]
    if len(to_addresses) == 1:
        msg['To'] = formataddr((to_name, to_addresses[0])) if to_name else to_addresses[0]
    else:
        # Multiple To: recipients — to_name only applies to first
        msg['To'] = ', '.join(to_addresses)

    msg['Subject'] = subject
    msg['Message-ID'] = msg_id
    if in_reply_to:
        msg['In-Reply-To'] = in_reply_to
    if references:
        msg['References'] = references
    if cc:
        msg['Cc'] = cc
    # BCC is intentionally NOT added as a header — recipients added to RCPT only

    # Build full recipients list: To + CC + BCC
    all_recipients = list(to_addresses)
    if cc:
        all_recipients += [a.strip() for a in cc.split(',') if a.strip()]
    if bcc:
        all_recipients += [a.strip() for a in bcc.split(',') if a.strip()]

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(config.email_address, app_password)
            server.sendmail(config.email_address, all_recipients, msg.as_string())
        return True, '', msg_id
    except smtplib.SMTPAuthenticationError:
        return False, 'Autenticação SMTP falhou. Verifica o endereço e a App Password.', ''
    except smtplib.SMTPRecipientsRefused:
        return False, f'Endereço de destinatário recusado: {to_email}', ''
    except smtplib.SMTPException as e:
        logger.error('SMTP error: %s', e)
        return False, f'Erro SMTP: {e}', ''
    except OSError as e:
        logger.error('Network error sending email: %s', e)
        return False, f'Erro de rede: {e}', ''


# ---------------------------------------------------------------------------
# Email Layout — envelope wrapper
# ---------------------------------------------------------------------------

def _get_initials(name: str) -> str:
    """Retorna as iniciais de um nome (máximo 2 caracteres)."""
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[0].upper() if name else '?'


def _build_company_address(company) -> str:
    """Constrói a morada curta para o header (Rua · Código Postal Cidade)."""
    parts = []
    if company.address:
        # Primeira linha da morada
        parts.append(company.address.split('\n')[0].strip())
    if company.postal_code or company.city:
        location = ' '.join(filter(None, [company.postal_code, company.city]))
        if location:
            parts.append(location)
    if company.country:
        parts.append(company.country)
    return ' · '.join(parts) if parts else ''


def _build_company_full_address(company) -> str:
    """Constrói a morada completa para o footer."""
    parts = []
    if company.address:
        parts.append(company.address.replace('\n', ' · ').strip())
    location = ' '.join(filter(None, [company.postal_code, company.city]))
    if location:
        parts.append(location)
    if company.country:
        parts.append(company.country)
    return ' · '.join(parts) if parts else ''


def _get_record_label(record) -> str:
    """Gera um label legível para o registo (ex: 'Lead: Proposta Website')."""
    model_name = record.__class__.__name__
    display = str(record)
    return f'{model_name}: {display}'


def _strip_website_protocol(url: str) -> str:
    """Remove https:// ou http:// do URL para exibição."""
    if not url:
        return ''
    return url.replace('https://', '').replace('http://', '').rstrip('/')


def wrap_email_with_layout(body_html: str, user, record=None, subject: str = '') -> str:
    """
    Envolve o conteúdo HTML do email com o layout (envelope) global.

    Lê o HTML do EmailLayout guardado na BD e substitui os placeholders
    Django template com os dados reais do utilizador, empresa e registo.

    Se não existir layout na BD, devolve o body_html original (sem envelope).

    Args:
        body_html: Conteúdo HTML do email (corpo).
        user:      Utilizador que envia o email.
        record:    Instância do modelo ligado (Lead, Contact, etc.) — opcional.
        subject:   Assunto do email.

    Returns:
        HTML completo com o envelope aplicado.
    """
    from django.template import Template, Context
    from django.utils import timezone
    from django.utils.safestring import mark_safe
    from apps.core.models import EmailLayout

    layout = EmailLayout.get_layout()
    if not layout:
        logger.warning('EmailLayout não encontrado na BD. Email enviado sem envelope.')
        return body_html

    # ── Dados da empresa ──
    company = getattr(user, 'default_company', None)
    if not company:
        companies = getattr(user, 'companies', None)
        if companies:
            company = companies.first()

    company_name = company.name if company else ''
    company_initial = company_name[0].upper() if company_name else '?'
    company_address = _build_company_address(company) if company else ''
    company_full_address = _build_company_full_address(company) if company else ''

    company_logo_url = ''
    inline_images = []
    if company and company.logo:
        try:
            # Ler bytes do logo para embutir como inline CID no email
            logo_path = company.logo.path
            import mimetypes as _mt
            mime = _mt.guess_type(logo_path)[0] or 'image/png'
            with open(logo_path, 'rb') as f:
                logo_bytes = f.read()
            if logo_bytes:
                company_logo_url = 'cid:company_logo'
                inline_images.append({
                    'cid': 'company_logo',
                    'content': logo_bytes,
                    'mime_type': mime,
                })
        except (ValueError, FileNotFoundError, OSError) as e:
            logger.warning('Não foi possível ler o logo da empresa: %s', e)

    # ── Dados do remetente ──
    sender_name = user.get_full_name() or user.username
    sender_initials = _get_initials(sender_name)
    sender_email = ''
    try:
        sender_email = user.email_config.email_address
    except Exception:
        sender_email = user.email or ''

    sender_phone = getattr(user, 'phone', '') or ''
    sender_role = ''
    if hasattr(user, 'get_role_display'):
        sender_role = user.get_role_display()

    # ── Dados do registo ──
    record_label = _get_record_label(record) if record else ''
    date_sent = timezone.now().strftime('%d/%m/%Y')

    # ── Dados do website da empresa ──
    company_website = company.website if company else ''
    company_website_display = _strip_website_protocol(company_website)

    # ── Contexto para o template ──
    context = Context({
        'subject': subject,
        'body_content': mark_safe(body_html),
        # Empresa
        'company_name': company_name,
        'company_initial': company_initial,
        'company_logo_url': company_logo_url,
        'company_address': company_address,
        'company_full_address': company_full_address,
        'company_email': company.email if company else '',
        'company_phone': company.phone if company else '',
        'company_website': company_website,
        'company_website_display': company_website_display,
        # Remetente
        'sender_name': sender_name,
        'sender_initials': sender_initials,
        'sender_email': sender_email,
        'sender_phone': sender_phone,
        'sender_role': sender_role,
        # Registo
        'record_label': record_label,
        'date_sent': date_sent,
    })

    try:
        template = Template(layout.html_content)
        rendered = template.render(context)
        return rendered, inline_images
    except Exception as e:
        logger.error('Erro ao renderizar EmailLayout: %s', e)
        return body_html, inline_images


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def send_email_for_record(
    user,
    record,
    to_email: str,
    subject: str,
    body: str,
    body_html=None,
    to_name: str = '',
    attachments=None,
    cc: str = '',
    bcc: str = '',
    in_reply_to: str = '',
    references: str = '',
) -> dict:
    """
    Envia um email em nome de `user` para `to_email` e regista-o como
    ChatterMessage (message_type='EMAIL') ligado a `record` via GenericForeignKey.

    Args:
        user:      Utilizador que envia (deve ter UserEmailConfig configurado).
        record:    Qualquer instância de modelo Django (Lead, Purchase, etc.).
        to_email:  Email do destinatário.
        subject:   Assunto.
        body:      Corpo em texto simples.
        body_html: Corpo em HTML (opcional — cria multipart/alternative).
        to_name:   Nome de apresentação do destinatário (opcional).

    Returns:
        {'success': True, 'message_id': '<...>'} ou
        {'success': False, 'error': '<mensagem>'}
    """
    try:
        config = user.email_config
    except Exception:
        return {
            'success': False,
            'error': 'Não tens email configurado. Vai às definições do teu perfil e configura o email de envio.',
        }

    if not config.is_active:
        return {'success': False, 'error': 'A tua configuração de email está desativada.'}

    if not config.has_smtp_configured:
        return {
            'success': False,
            'error': 'Configura o email de envio e a App Password no teu perfil antes de enviar.',
        }

    sender_name = user.get_full_name() or user.username

    # ── Envolver o HTML com o layout (envelope) ──
    wrapped_html = body_html
    inline_images = []
    if body_html:
        wrapped_html, inline_images = wrap_email_with_layout(
            body_html=body_html,
            user=user,
            record=record,
            subject=subject,
        )

    success, error, msg_id = _send_via_smtp(
        config=config,
        to_email=to_email,
        subject=subject,
        body=body,
        body_html=wrapped_html,
        to_name=to_name,
        sender_name=sender_name,
        attachments=attachments or [],
        cc=cc,
        bcc=bcc,
        in_reply_to=in_reply_to,
        references=references,
        inline_images=inline_images,
    )

    if not success:
        return {'success': False, 'error': error}

    # Primary recipient for DB (EmailField accepts one address)
    primary_to = to_email.split(',')[0].strip()

    # Metadados para BD (sem os bytes de conteúdo)
    att_meta = [
        {k: v for k, v in att.items() if k != 'content'}
        for att in (attachments or [])
    ]

    from django.contrib.contenttypes.models import ContentType
    from apps.core.models import ChatterMessage
    from django.utils import timezone

    ct = ContentType.objects.get_for_model(record.__class__)
    ChatterMessage.objects.create(
        content_type=ct,
        object_id=record.pk,
        author=user,
        message_type='EMAIL',
        subject=subject,
        body=body,
        body_html=body_html or '',
        from_email=config.email_address,
        to_email=primary_to,
        cc_emails=cc,
        bcc_emails=bcc,
        direction=ChatterMessage.DIRECTION_OUTBOUND,
        message_id=msg_id,
        in_reply_to=in_reply_to,
        sent_at=timezone.now(),
        is_internal=False,
        attachments=att_meta,
    )

    logger.info(
        'Email sent by %s to %s (record=%s pk=%s subject=%s attachments=%d)',
        user.username, to_email, record.__class__.__name__, record.pk, subject,
        len(attachments or []),
    )
    return {'success': True, 'message_id': msg_id}


# ---------------------------------------------------------------------------
# IMAP — polling de respostas inbound
# ---------------------------------------------------------------------------

def _decode_header_value(value: str) -> str:
    """Descodifica um header MIME (pode estar encoded como =?utf-8?...?)."""
    import email.header
    if not value:
        return ''
    decoded_parts = email.header.decode_header(value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or 'utf-8', errors='replace'))
        else:
            result.append(part)
    return ' '.join(result)


def _parse_email_body(msg) -> str:
    """Extrai o corpo em texto simples de uma mensagem email.message.Message."""
    body_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get('Content-Disposition', ''))
            if ct == 'text/plain' and 'attachment' not in cd:
                charset = part.get_content_charset() or 'utf-8'
                try:
                    body_parts.append(
                        part.get_payload(decode=True).decode(charset, errors='replace')
                    )
                except Exception:
                    body_parts.append(
                        part.get_payload(decode=True).decode('utf-8', errors='replace')
                    )
    else:
        charset = msg.get_content_charset() or 'utf-8'
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                body_parts.append(payload.decode(charset, errors='replace'))
        except Exception:
            pass
    return '\n'.join(body_parts).strip()


def _parse_email_html(msg) -> str:
    """Extrai o corpo HTML de uma mensagem email.message.Message."""
    html_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get('Content-Disposition', ''))
            if ct == 'text/html' and 'attachment' not in cd:
                charset = part.get_content_charset() or 'utf-8'
                try:
                    html_parts.append(
                        part.get_payload(decode=True).decode(charset, errors='replace')
                    )
                except Exception:
                    html_parts.append(
                        part.get_payload(decode=True).decode('utf-8', errors='replace')
                    )
    else:
        if msg.get_content_type() == 'text/html':
            charset = msg.get_content_charset() or 'utf-8'
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    html_parts.append(payload.decode(charset, errors='replace'))
            except Exception:
                pass
    return _strip_quoted_html('\n'.join(html_parts).strip())


def _strip_quoted_html(html: str) -> str:
    """
    Remove blocos de citação/thread do corpo HTML de um email de resposta.
    Corta tudo a partir do primeiro marcador de quote reconhecido
    (Gmail, Outlook, Apple Mail), que é sempre no fim da mensagem.
    """
    import re

    QUOTE_START_PATTERNS = [
        r'<div\s[^>]*class="[^"]*gmail_quote[^"]*"',   # Gmail quote block
        r'<div\s[^>]*class="[^"]*gmail_attr[^"]*"',    # Gmail "X wrote:" header
        r'<div\s[^>]*id=["\']divRplyFwdMsg["\']',       # Outlook reply header
        r'<div\s[^>]*id=["\']divTaggedContent["\']',    # Outlook tagged content
        r'<blockquote\s[^>]*type=["\']cite["\']',       # Apple Mail
        r'<hr\s[^>]*id=["\']stopSpelling["\']',         # Outlook HR separator
        r'<!--\s*---->.*?$',                             # Outlook comment separator
    ]

    for pattern in QUOTE_START_PATTERNS:
        m = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if m:
            html = html[:m.start()].rstrip()

    return html.strip()


def _strip_quoted_reply(body: str) -> str:
    """
    Remove o texto quotado de uma resposta de email.

    Suporta os formatos mais comuns:
      - Gmail PT: "cubix <...> escreveu (data àS hora):"
      - Gmail EN: "On Mon, dd MMM yyyy at hh:mm, ... wrote:"
      - Outlook:  "-----Original Message-----" / "________________________________"
      - Linhas prefixadas com ">" (resposta standard RFC)
    """
    import re

    # Padrões que marcam o início do texto quotado (numa linha ou em duas)
    QUOTE_PATTERNS = [
        # Gmail PT: "Nome <email> escreveu (data):"
        r'^\s*.+<.+>\s+escreveu\s*\(',
        # Gmail EN: "On ..., ... wrote:"
        r'^\s*On\s.+wrote\s*:',
        # Outlook PT/EN: separador de linha
        r'^\s*-{3,}\s*(Original Message|Mensagem Original)\s*-{3,}',
        r'^\s*_{10,}\s*$',
        # Apple Mail / outros
        r'^\s*>{1,}\s*From\s*:',
    ]
    quote_re = re.compile('|'.join(QUOTE_PATTERNS), re.IGNORECASE)

    lines = body.splitlines()
    cutoff = None

    i = 0
    while i < len(lines):
        line = lines[i]
        # Linha `>` sozinha ou precedida de espaço — início de bloco quotado
        if re.match(r'^\s*>\s*', line):
            # Só corta se TODOS os restantes forem quotados ou vazios
            rest = lines[i:]
            if all(re.match(r'^\s*>\s*', l) or l.strip() == '' for l in rest):
                cutoff = i
                break
        # Padrão de cabeçalho de resposta
        if quote_re.match(line):
            cutoff = i
            break
        # Gmail divide "Name wrote:" em duas linhas às vezes
        if i + 1 < len(lines):
            two_lines = line + ' ' + lines[i + 1]
            if quote_re.match(two_lines):
                cutoff = i
                break
        i += 1

    if cutoff is not None:
        trimmed = '\n'.join(lines[:cutoff]).rstrip()
    else:
        trimmed = body.rstrip()

    return trimmed


def poll_imap_replies_for_user(config, known_message_ids=None) -> list:
    """
    Liga-se ao IMAP do utilizador e procura respostas a emails que enviámos.

    Args:
        config:             UserEmailConfig (credenciais SMTP/IMAP).
        known_message_ids:  set de Message-IDs dos nossos emails outbound.
                            Se None, devolve todas as mensagens recentes
                            (útil para diagnóstico; normalmente passa-se sempre o set).

    Returns:
        Lista de dicts — cada um é um email inbound encontrado:
        {
            'imap_message_id': str,
            'in_reply_to':     str,
            'references':      str,
            'from_email':      str,
            'subject':         str,
            'body':            str,
            'date':            datetime,
        }
    """
    import imaplib
    import email as email_lib
    import re
    from datetime import datetime, timedelta
    from email.utils import parseaddr, parsedate_to_datetime
    from django.utils import timezone

    imap_cfg = IMAP_PROVIDERS.get(config.provider, IMAP_PROVIDERS['gmail'])

    try:
        app_password = decrypt_password(config.app_password)
    except ValueError as e:
        logger.error('IMAP: falha ao desencriptar password para %s: %s', config.email_address, e)
        return []

    results = []
    try:
        with imaplib.IMAP4_SSL(imap_cfg['host'], imap_cfg['port']) as imap:
            imap.login(config.email_address, app_password)
            imap.select('INBOX', readonly=True)

            # Pesquisar mensagens dos últimos 30 dias
            since = (datetime.utcnow() - timedelta(days=30)).strftime('%d-%b-%Y')
            status, data = imap.search(None, f'SINCE {since}')
            if status != 'OK' or not data or not data[0]:
                return []

            msg_nums = data[0].split()
            # Limitar a 200 mensagens mais recentes para não sobrecarregar
            for num in msg_nums[-200:]:
                # Buscar apenas os headers relevantes primeiro (PEEK = não marca como lido)
                status, header_data = imap.fetch(
                    num,
                    '(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID IN-REPLY-TO REFERENCES FROM SUBJECT DATE)])'
                )
                if status != 'OK' or not header_data or not isinstance(header_data[0], tuple):
                    continue

                parsed = email_lib.message_from_bytes(header_data[0][1])
                imap_mid    = (parsed.get('Message-ID')  or '').strip()
                in_reply_to = (parsed.get('In-Reply-To') or '').strip()
                references  = (parsed.get('References')  or '').strip()

                # Filtrar: apenas respostas aos nossos emails
                if known_message_ids is not None:
                    reply_ids = set(re.findall(r'<[^>]+>', in_reply_to))
                    reply_ids.update(re.findall(r'<[^>]+>', references))
                    if not reply_ids.intersection(known_message_ids):
                        continue

                # Buscar a mensagem completa para extrair o body
                status, body_data = imap.fetch(num, '(RFC822)')
                if status != 'OK' or not body_data or not isinstance(body_data[0], tuple):
                    continue

                full_msg = email_lib.message_from_bytes(body_data[0][1])

                from_header = _decode_header_value(full_msg.get('From', ''))
                _, from_addr = parseaddr(from_header)

                # Ignorar emails que foram enviados pelo próprio utilizador
                # (ex: enviou para si próprio em teste, ou email saiu para Sent/Inbox)
                if from_addr.lower() == config.email_address.lower():
                    continue

                subject = _decode_header_value(full_msg.get('Subject', ''))

                try:
                    date = parsedate_to_datetime(full_msg.get('Date', ''))
                    # Tornar timezone-aware se necessário (stdlib, sem pytz)
                    if date.tzinfo is None:
                        from datetime import timezone as _utc
                        date = date.replace(tzinfo=_utc.utc)
                except Exception:
                    date = timezone.now()

                raw_body = _parse_email_body(full_msg)
                body = _strip_quoted_reply(raw_body)
                body_html = _parse_email_html(full_msg)

                results.append({
                    'imap_message_id': imap_mid,
                    'in_reply_to'    : in_reply_to,
                    'references'     : references,
                    'from_email'     : from_addr,
                    'subject'        : subject,
                    'body'           : body,
                    'body_html'      : body_html,
                    'date'           : date,
                })

    except imaplib.IMAP4.error as e:
        logger.error('IMAP error para %s: %s', config.email_address, e)
    except OSError as e:
        logger.error('IMAP network error para %s: %s', config.email_address, e)
    except Exception as e:
        logger.exception('IMAP erro inesperado para %s: %s', config.email_address, e)

    return results
