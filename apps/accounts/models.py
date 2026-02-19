from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


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
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
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
