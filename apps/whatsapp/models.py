from django.db import models
from django.conf import settings
from apps.core.models import AbstractBaseModel


class WhatsAppTemplate(AbstractBaseModel):
    """
    Modelo para templates do WhatsApp Business API (Meta).
    Cada template tem de ser submetido à Meta para aprovação antes de poder ser usado
    para contactar clientes que ainda não iniciaram conversa.

    Workflow:
        DRAFT → (submeter à API) → PENDING → APPROVED / REJECTED / PAUSED
    """

    # --- Categorias (exigidas pela Meta) ---
    CATEGORY_AUTHENTICATION = 'AUTHENTICATION'
    CATEGORY_MARKETING = 'MARKETING'
    CATEGORY_UTILITY = 'UTILITY'
    CATEGORY_CHOICES = [
        (CATEGORY_AUTHENTICATION, 'Autenticação'),
        (CATEGORY_MARKETING, 'Marketing'),
        (CATEGORY_UTILITY, 'Utilidade'),
    ]

    # --- Idiomas suportados ---
    LANGUAGE_CHOICES = [
        ('pt_PT', 'Português (Portugal)'),
        ('pt_BR', 'Português (Brasil)'),
        ('en_US', 'Inglês (EUA)'),
        ('en_GB', 'Inglês (Reino Unido)'),
        ('fr', 'Francês'),
        ('es', 'Espanhol'),
        ('de', 'Alemão'),
        ('it', 'Italiano'),
        ('nl', 'Neerlandês'),
        ('ar', 'Árabe'),
        ('zh_CN', 'Chinês (Simplificado)'),
    ]

    # --- Estado do template (devolvido pela Meta) ---
    STATUS_DRAFT = 'DRAFT'
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_PAUSED = 'PAUSED'
    STATUS_DISABLED = 'DISABLED'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Rascunho'),
        (STATUS_PENDING, 'Pendente'),
        (STATUS_APPROVED, 'Aprovado'),
        (STATUS_REJECTED, 'Rejeitado'),
        (STATUS_PAUSED, 'Pausado'),
        (STATUS_DISABLED, 'Desativado'),
    ]

    # --- Tipo de cabeçalho ---
    HEADER_NONE = 'NONE'
    HEADER_TEXT = 'TEXT'
    HEADER_IMAGE = 'IMAGE'
    HEADER_VIDEO = 'VIDEO'
    HEADER_DOCUMENT = 'DOCUMENT'
    HEADER_CHOICES = [
        (HEADER_NONE, 'Sem cabeçalho'),
        (HEADER_TEXT, 'Texto'),
        (HEADER_IMAGE, 'Imagem'),
        (HEADER_VIDEO, 'Vídeo'),
        (HEADER_DOCUMENT, 'Documento'),
    ]

    # --- Modelo de negócio associado (para mapeamento de variáveis) ---
    MODEL_CHOICES = [
        ('', 'Sem modelo específico'),
        ('crm.Lead', 'CRM — Prospecto/Lead'),
        ('sales.SaleOrder', 'Vendas — Orçamento/Venda'),
        ('purchases.PurchaseOrder', 'Compras — Encomenda'),
        ('financial.Invoice', 'Financeiro — Fatura'),
    ]

    # ---------------------------------------------------------------
    # Campos de identificação
    # ---------------------------------------------------------------
    name = models.CharField(
        max_length=512,
        unique=True,
        verbose_name='Nome técnico',
        help_text='Nome único em lowercase com underscores (ex: orcamento_aprovado). '
                  'Não pode ser alterado após submissão à Meta.',
    )
    display_name = models.CharField(
        max_length=255,
        verbose_name='Nome apresentado',
        help_text='Nome legível para o utilizador (ex: Orçamento Aprovado).',
    )

    # ---------------------------------------------------------------
    # Classificação
    # ---------------------------------------------------------------
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_MARKETING,
        verbose_name='Categoria',
        help_text='A categoria determina o custo de envio e as regras da Meta.',
    )
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='pt_PT',
        verbose_name='Idioma',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name='Estado',
        help_text='Estado de aprovação devolvido pela Meta.',
    )
    allow_category_change = models.BooleanField(
        default=True,
        verbose_name='Permitir alteração de categoria',
        help_text='Permite à Meta reclassificar o template se necessário.',
    )

    # ---------------------------------------------------------------
    # Cabeçalho (Header)
    # ---------------------------------------------------------------
    header_type = models.CharField(
        max_length=20,
        choices=HEADER_CHOICES,
        default=HEADER_NONE,
        verbose_name='Tipo de cabeçalho',
    )
    header_text = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='Texto do cabeçalho',
        help_text='Apenas quando o tipo de cabeçalho é "Texto". Máx. 60 caracteres.',
    )

    # ---------------------------------------------------------------
    # Corpo (Body) — campo principal
    # ---------------------------------------------------------------
    body = models.TextField(
        verbose_name='Corpo da mensagem',
        help_text='Texto da mensagem. Use {{1}}, {{2}}, … para variáveis dinâmicas.',
    )

    # ---------------------------------------------------------------
    # Rodapé (Footer)
    # ---------------------------------------------------------------
    footer = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='Rodapé',
        help_text='Texto pequeno no final da mensagem. Máx. 60 caracteres.',
    )

    # ---------------------------------------------------------------
    # Botões
    # ---------------------------------------------------------------
    buttons = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Botões',
        help_text=(
            'Lista de botões. Exemplos:\n'
            '  URL: {"type": "URL", "text": "Ver orçamento", "url": "https://..."}\n'
            '  PHONE_NUMBER: {"type": "PHONE_NUMBER", "text": "Ligar", "phone_number": "+351..."}\n'
            '  QUICK_REPLY: {"type": "QUICK_REPLY", "text": "Confirmar"}\n'
            '  COPY_CODE: {"type": "COPY_CODE", "example": "ABC123"}'
        ),
    )

    # ---------------------------------------------------------------
    # Mapeamento de variáveis
    # ---------------------------------------------------------------
    variables = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Mapeamento de variáveis',
        help_text=(
            'Mapeia cada variável {{N}} ao campo do modelo. Exemplo:\n'
            '{"1": "contact.name", "2": "title", "3": "estimated_value"}'
        ),
    )
    model_name = models.CharField(
        max_length=100,
        blank=True,
        choices=MODEL_CHOICES,
        verbose_name='Modelo associado',
        help_text='Modelo de Django ao qual este template se aplica (para mapeamento de variáveis).',
    )

    # ---------------------------------------------------------------
    # Meta API
    # ---------------------------------------------------------------
    wa_template_uid = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='ID WhatsApp (Meta)',
        help_text='ID devolvido pela Meta após a submissão. Preenchido automaticamente.',
    )

    # ---------------------------------------------------------------
    # Multi-empresa
    # ---------------------------------------------------------------
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='whatsapp_templates',
        verbose_name='Empresa',
        help_text='Empresa proprietária deste template. NULL = global.',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='whatsapp_templates_created',
        verbose_name='Criado por',
    )

    class Meta:
        verbose_name = 'Template WhatsApp'
        verbose_name_plural = 'Templates WhatsApp'
        ordering = ['display_name']

    def __str__(self):
        return f'{self.display_name} [{self.get_language_display()}] — {self.get_status_display()}'

    @property
    def status_color(self):
        """Tailwind color class for badge."""
        return {
            self.STATUS_DRAFT: 'gray',
            self.STATUS_PENDING: 'yellow',
            self.STATUS_APPROVED: 'green',
            self.STATUS_REJECTED: 'red',
            self.STATUS_PAUSED: 'orange',
            self.STATUS_DISABLED: 'red',
        }.get(self.status, 'gray')

    @property
    def variable_count(self):
        """Number of variables in the body."""
        import re
        return len(re.findall(r'\{\{\d+\}\}', self.body))
