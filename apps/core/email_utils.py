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
from email.utils import formataddr, make_msgid

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
                   body_html, to_name: str, sender_name: str):
    """
    Envia o email e devolve (success: bool, error: str, message_id: str).
    Não escreve nada na BD.
    """
    provider = SMTP_PROVIDERS.get(config.provider, SMTP_PROVIDERS['gmail'])
    smtp_host = provider['host']
    smtp_port = provider['port']

    try:
        app_password = decrypt_password(config.app_password)
    except ValueError as e:
        return False, str(e), ''

    msg_id = make_msgid(domain=config.email_address.split('@')[-1])

    if body_html:
        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        msg.attach(MIMEText(body_html, 'html', 'utf-8'))
    else:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

    msg['From'] = formataddr((sender_name, config.email_address))
    msg['To'] = formataddr((to_name, to_email)) if to_name else to_email
    msg['Subject'] = subject
    msg['Message-ID'] = msg_id

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(config.email_address, app_password)
            server.sendmail(config.email_address, [to_email], msg.as_string())
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

    success, error, msg_id = _send_via_smtp(
        config=config,
        to_email=to_email,
        subject=subject,
        body=body,
        body_html=body_html,
        to_name=to_name,
        sender_name=sender_name,
    )

    if not success:
        return {'success': False, 'error': error}

    # Guardar no chatter (funciona com qualquer modelo via GenericForeignKey)
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
        from_email=config.email_address,
        to_email=to_email,
        direction=ChatterMessage.DIRECTION_OUTBOUND,
        message_id=msg_id,
        sent_at=timezone.now(),
        is_internal=False,
    )

    logger.info(
        'Email sent by %s to %s (record=%s pk=%s subject=%s)',
        user.username, to_email, record.__class__.__name__, record.pk, subject,
    )
    return {'success': True, 'message_id': msg_id}
