from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# ---------------------------------------------------------------------------
# App Permission Registry
# Adiciona aqui cada aplicação que deverá ter controlo de acesso por utilizador.
# Chave (slug) deve corresponder ao nome usado nos decoradors require_app_role().
# ---------------------------------------------------------------------------
APP_REGISTRY = [
    ('crm',       'CRM / Leads & Pipeline'),
    ('contacts',  'Contactos'),
    ('inventory', 'Inventário'),
    ('purchases', 'Compras'),
    ('sales',     'Vendas'),
    ('website',   'Website'),
    ('financial', 'Financeiro'),
    ('bom',       'BOM'),
    ('documents', 'Documentos'),
    ('marketing', 'Marketing'),
    ('reports',   'Relatórios'),
]

# ---------------------------------------------------------------------------
# Mapa app slug -> modelos (app_label, model_name, nome display)
# Usado para construir o accordion de permissões CRUD por tabela.
# Adiciona aqui novos modelos quando forem criados.
# ---------------------------------------------------------------------------
APP_MODELS_REGISTRY = {
    'crm': [
        ('crm', 'crmtag',   'Tags'),
        ('crm', 'crmstage', 'Etapas'),
        ('crm', 'lead',     'Leads'),
        ('crm', 'activity', 'Atividades'),
        ('crm', 'leadnote', 'Notas'),
    ],
    'contacts': [
        ('contacts', 'contacttag', 'Tags de Contacto'),
        ('contacts', 'contact',    'Contactos'),
    ],
}


class CustomUser(AbstractUser):
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    EMPLOYEE = 'EMPLOYEE'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,20}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 20 digits allowed."
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True,
        null=True
    )
    
    avatar = models.TextField(
        blank=True,
        null=True,
        help_text='Imagem do avatar em formato base64 (data URL)'
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=EMPLOYEE
    )
    
    # Multi-company support
    companies = models.ManyToManyField(
        'core.Company',
        related_name='users',
        blank=True,
        verbose_name='Companies'
    )
    
    default_company = models.ForeignKey(
        'core.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_users',
        verbose_name='Default Company'
    )

    # Two-Factor Authentication (TOTP / Google Authenticator)
    totp_secret = models.CharField(
        max_length=64,
        blank=True,
        default='',
        help_text='Base32 secret for TOTP 2FA'
    )
    totp_enabled = models.BooleanField(
        default=False,
        help_text='Whether 2FA is active for this user'
    )

    def get_full_name(self):
        full_name = super().get_full_name()
        return full_name if full_name else self.username
    
    def __str__(self):
        return self.username


class UserEmailConfig(models.Model):
    """
    Configuração SMTP por utilizador.

    Centraliza as credenciais de envio de email de cada utilizador.
    Utilizado pelo sistema de chatter para enviar emails a partir de
    qualquer módulo (Leads, Compras, Vendas, etc.).

    A app_password é armazenada encriptada com Fernet (settings.FERNET_KEY).
    Para gerar uma App Password Gmail: https://myaccount.google.com/apppasswords
    Para Outlook: https://account.microsoft.com/security
    """

    PROVIDER_GMAIL = 'gmail'
    PROVIDER_OUTLOOK = 'outlook'
    PROVIDER_CHOICES = [
        (PROVIDER_GMAIL, 'Gmail'),
        (PROVIDER_OUTLOOK, 'Outlook / Microsoft 365'),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='email_config',
        verbose_name='Utilizador',
    )
    email_address = models.EmailField(
        verbose_name='Email de envio (SMTP)',
        help_text='Endereço de email utilizado para enviar mensagens. Ex: joao@gmail.com',
    )
    app_password = models.TextField(
        verbose_name='App Password (encriptada)',
        help_text=(
            'App Password gerada na conta Google/Microsoft. '
            'Nunca é a password principal — é uma password específica para aplicações. '
            'Armazenada de forma encriptada.'
        ),
    )
    provider = models.CharField(
        max_length=10,
        choices=PROVIDER_CHOICES,
        default=PROVIDER_GMAIL,
        verbose_name='Provedor SMTP',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Se desativado, o envio de emails fica suspenso para este utilizador.',
    )

    class Meta:
        verbose_name = 'Configuração de Email'
        verbose_name_plural = 'Configurações de Email'

    @property
    def has_smtp_configured(self) -> bool:
        """True quando o utilizador tem email e app password configurados."""
        return bool(self.email_address and self.app_password)

    def __str__(self):
        return f'{self.user.username} — {self.email_address} ({self.get_provider_display()})'


# ---------------------------------------------------------------------------
# App-level Role Permissions
# ---------------------------------------------------------------------------

class AppRole(models.Model):
    """
    Permissão de um utilizador numa aplicação específica, por empresa.

    Níveis:
        readonly — pode ver registos (de todos), sem criar/editar/apagar
        user     — pode criar e editar os seus próprios registos; sem configurações
        manager  — pode criar/editar/apagar todos os registos + acesso a configurações
        admin    — acesso total (equivalente a manager + gestão de utilizadores da app)
    """
    READONLY = 'readonly'
    USER     = 'user'
    MANAGER  = 'manager'
    ADMIN    = 'admin'

    LEVEL_CHOICES = [
        (READONLY, 'Read Only'),
        (USER,     'Utilizador'),
        (MANAGER,  'Manager'),
        (ADMIN,    'Admin'),
    ]

    LEVEL_ORDER = {READONLY: 0, USER: 1, MANAGER: 2, ADMIN: 3}

    user    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='app_roles',
        verbose_name='Utilizador',
    )
    app     = models.CharField(max_length=50, verbose_name='Aplicação')
    company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        related_name='user_app_roles',
        verbose_name='Empresa',
    )
    level   = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='Nível')

    class Meta:
        unique_together = ('user', 'app', 'company')
        verbose_name = 'Permissão de Aplicação'
        verbose_name_plural = 'Permissões de Aplicação'
        ordering = ['user', 'company', 'app']

    def __str__(self):
        return f'{self.user} — {self.app} [{self.level}] @ {self.company}'
