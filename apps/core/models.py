import uuid
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
    
    def __str__(self):
        return f"{self.action} - {self.model_name} ({self.object_id}) by {self.user}"


class ErrorLog(models.Model):
    LEVEL_CHOICES = [
        ('ERROR', 'Error'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    ]
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    traceback = models.TextField(blank=True, null=True)
    request_path = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Error Log'
        verbose_name_plural = 'Error Logs'
    
    def __str__(self):
        return f"{self.level} - {self.message[:50]} at {self.timestamp}"


class Company(AbstractBaseModel):
    """
    Multi-company model for system-wide company management.
    Allows multiple companies in the same system with shared users.
    """
    # Basic Information
    name = models.CharField(max_length=255, unique=True, verbose_name='Company Name')
    legal_name = models.CharField(max_length=255, blank=True, verbose_name='Legal Name')
    vat = models.CharField(max_length=20, blank=True, verbose_name='VAT/NIF')
    company_registry = models.CharField(max_length=50, blank=True, verbose_name='Company Registry Number')
    
    # Contact Information
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Phone')
    website = models.URLField(max_length=255, blank=True, verbose_name='Website')
    
    # Address
    address = models.TextField(blank=True, verbose_name='Address')
    city = models.CharField(max_length=100, blank=True, verbose_name='City')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Postal Code')
    country = models.CharField(max_length=100, default='Portugal', verbose_name='Country')
    
    # Regional Settings
    currency = models.CharField(max_length=3, default='EUR', verbose_name='Default Currency')
    language = models.CharField(max_length=10, default='pt_PT', verbose_name='Default Language')
    
    # Branding
    logo = models.ImageField(upload_to='companies/logos/', blank=True, null=True, verbose_name='Company Logo')
    
    # Hierarchy (for company groups)
    parent_company = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subsidiaries',
        verbose_name='Parent Company'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.name
    
    @property
    def is_subsidiary(self):
        """Check if this company is a subsidiary of another"""
        return self.parent_company is not None


class ChatterMessage(AbstractBaseModel):
    """
    Universal message system for emails and internal notes.
    Uses GenericForeignKey to work with ANY Django model (Lead, Contact, Sale, etc.)
    
    Usage:
        # Create note for Lead
        ChatterMessage.objects.create(
            content_object=lead,
            author=user,
            message_type='NOTE',
            body='Important note about this lead'
        )
        
        # Create email for Contact
        ChatterMessage.objects.create(
            content_object=contact,
            author=user,
            message_type='EMAIL',
            subject='Follow up',
            body='Email content...',
            to_email=contact.email
        )
    """
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    
    # GenericForeignKey - works with ANY model
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Message Details
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chatter_messages',
        verbose_name='Author'
    )
    
    MESSAGE_TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('NOTE', 'Internal Note'),
    ]
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        default='NOTE',
        verbose_name='Message Type'
    )
    
    subject = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Subject',
        help_text='Only for emails'
    )
    body = models.TextField(verbose_name='Message Body')
    
    # Email specific fields
    to_email = models.EmailField(blank=True, null=True, verbose_name='To')
    cc_emails = models.TextField(
        blank=True,
        verbose_name='CC',
        help_text='Comma-separated email addresses'
    )
    
    # Attachments
    attachments = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Attachments',
        help_text='List of attachment objects: [{"filename": "file.pdf", "url": "/media/..."}]'
    )
    
    # Status
    is_internal = models.BooleanField(
        default=False,
        verbose_name='Is Internal Note',
        help_text='True = internal note, False = external communication'
    )
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Sent At',
        help_text='When the email was sent'
    )

    # --- Email threading fields (used when message_type='EMAIL') ---
    DIRECTION_OUTBOUND = 'outbound'
    DIRECTION_INBOUND = 'inbound'
    DIRECTION_CHOICES = [
        (DIRECTION_OUTBOUND, 'Enviado'),
        (DIRECTION_INBOUND, 'Recebido'),
    ]
    direction = models.CharField(
        max_length=8,
        choices=DIRECTION_CHOICES,
        default=DIRECTION_OUTBOUND,
        verbose_name='Direção',
        help_text='outbound = enviado pelo utilizador; inbound = recebido do cliente (IMAP futuro)',
    )
    from_email = models.EmailField(
        blank=True,
        verbose_name='De (email)',
        help_text='Remetente real do email — preenchido para outbound e inbound.',
    )
    message_id = models.CharField(
        max_length=998,
        blank=True,
        verbose_name='Message-ID',
        help_text='Header Message-ID SMTP. Utilizado para fazer match de respostas (IMAP futuro).',
    )
    in_reply_to = models.CharField(
        max_length=998,
        blank=True,
        verbose_name='In-Reply-To',
        help_text='Header In-Reply-To do email recebido. Permite ligar respostas à thread.',
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['author']),
            models.Index(fields=['message_type']),
        ]
        verbose_name = 'Chatter Message'
        verbose_name_plural = 'Chatter Messages'
    
    def __str__(self):
        return f"{self.get_message_type_display()} - {self.author} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_email(self):
        """Check if this is an email message"""
        return self.message_type == 'EMAIL'
    
    @property
    def is_note(self):
        """Check if this is an internal note"""
        return self.message_type == 'NOTE'


class ChatterActivity(models.Model):
    """
    Activity/Audit log for any Django model.
    Tracks all changes and actions on objects (Lead, Contact, Sale, etc.)
    
    Usage:
        # Log status change
        ChatterActivity.objects.create(
            content_object=lead,
            user=request.user,
            activity_type='STATUS_CHANGE',
            description='changed status from New to Qualified',
            details={'field': 'status', 'old': 'New', 'new': 'Qualified'}
        )
    """
    from django.contrib.contenttypes.fields import GenericForeignKey
    
    # GenericForeignKey - works with ANY model
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Activity Details
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chatter_activities',
        verbose_name='User'
    )
    
    ACTIVITY_TYPE_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
        ('STATUS_CHANGE', 'Status Changed'),
        ('STAGE_CHANGE', 'Stage Changed'),
        ('ASSIGNMENT', 'Assigned'),
        ('EMAIL_SENT', 'Email Sent'),
        ('WHATSAPP_SENT', 'WhatsApp Sent'),
        ('CALL', 'Phone Call'),
        ('MEETING', 'Meeting'),
        ('COMMENT', 'Comment'),
    ]
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        verbose_name='Activity Type'
    )
    
    description = models.TextField(
        verbose_name='Description',
        help_text='Human-readable description: "changed stage from New to Qualified"'
    )
    
    details = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Details',
        help_text='Structured data: {"field": "stage", "old_value": "New", "new_value": "Qualified"}'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
            models.Index(fields=['activity_type']),
        ]
        verbose_name = 'Chatter Activity'
        verbose_name_plural = 'Chatter Activities'
    
    def __str__(self):
        user_str = self.user.get_full_name() if self.user else 'System'
        return f"{user_str} - {self.get_activity_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ActivityType(AbstractBaseModel):
    """
    Tipo de atividade (ex: Phone Call, Email, WhatsApp).

    É apenas um rótulo reutilizável. O visual (SVG, cor) fica no blueprint
    (ScheduledActivity), porque vários blueprints do mesmo tipo podem ter
    ícones e cores diferentes.

    Exemplos de códigos: CALL, EMAIL, MEETING, TODO, WHATSAPP, DOCUMENT, SIGNATURE
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nome',
        help_text='Nome visível (ex: "Phone Call", "Email")'
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Código',
        help_text='Identificador único em maiúsculas (ex: CALL, EMAIL). Não alterar após criar workflows.'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Activity Type'
        verbose_name_plural = 'Activity Types'

    def __str__(self):
        return self.name


class ScheduledActivity(AbstractBaseModel):
    """
    Blueprint reutilizável de atividade.
    
    NÃO contém datas, responsáveis, resultados ou ligações a modelos.
    É apenas a definição do tipo de atividade que pode ser usada em cadeias.
    
    Os resultados/logs ficam em ActivityLog (por instância de cadeia).
    A ligação a Leads/Contacts fica em ActivityChainInstance.
    
    Usage:
        # Criar blueprint de atividade
        activity = ScheduledActivity.objects.create(
            activity_type=ActivityType.objects.get(code='CALL'),
            summary='Ligar ao cliente',
            description='Apresentar proposta e confirmar interesse',
            owner_company=company
        )
    """

    # Tipo de activity (FK para tabela ActivityType, gerida pelo utilizador)
    activity_type = models.ForeignKey(
        'ActivityType',
        on_delete=models.PROTECT,
        verbose_name='Activity Type',
        related_name='blueprints',
        null=True,
        blank=True,
    )
    
    # Nome identificador (label único para distinguir blueprints do mesmo tipo)
    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Name',
        help_text='Label para identificar o blueprint (ex: "Primeira Ligação", "Follow-up Email")'
    )

    # Conteúdo (definição do blueprint)
    summary = models.CharField(
        max_length=255,
        verbose_name='Summary',
        help_text='Título da atividade (ex: "Ligar ao cliente", "Enviar proposta")'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Descrição detalhada do que deve ser feito'
    )

    # Campos visuais (ícone e cor)
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Icon (FontAwesome ou Emoji)',
        help_text='Opcional: ícone FontAwesome (ex: fa-phone) ou Emoji (ex: 📞). Deixar vazio se usar SVG.'
    )
    icon_svg = models.TextField(
        blank=True,
        verbose_name='Icon SVG',
        help_text='SVG inline com currentColor para cor dinâmica'
    )
    icon_color = models.CharField(
        max_length=7,
        blank=True,
        default='#6366F1',
        verbose_name='Icon Color',
        help_text='Cor do ícone em hexadecimal (ex: #FF5733, #6366F1)'
    )
    DECORATION_TYPE_CHOICES = [
        ('', 'None'),
        ('warning', 'Warning (Orange)'),
        ('danger', 'Danger (Red)'),
        ('success', 'Success (Green)'),
        ('info', 'Info (Blue)'),
    ]
    decoration_type = models.CharField(
        max_length=20,
        choices=DECORATION_TYPE_CHOICES,
        blank=True,
        verbose_name='Decoration Type',
        help_text='Cor/estilo visual na interface'
    )

    # Multi-company
    owner_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='scheduled_activities',
        verbose_name='Owner Company'
    )

    class Meta:
        ordering = ['activity_type__name', 'name', 'summary']
        verbose_name = 'Scheduled Activity'
        verbose_name_plural = 'Scheduled Activities'

    def __str__(self):
        label = self.name or self.summary
        type_name = self.activity_type.name if self.activity_type else 'Sem Tipo'
        return f"{type_name} - {label}"

    @property
    def default_icon_emoji(self):
        """Emoji de fallback baseado no activity_type code"""
        if not self.activity_type:
            return '📋'
        icons = {
            'CALL': '📞',
            'EMAIL': '📧',
            'MEETING': '🤝',
            'TODO': '✅',
            'WHATSAPP': '💬',
            'DOCUMENT': '📄',
            'SIGNATURE': '✍️',
        }
        return icons.get(self.activity_type.code, '📋')

    def get_rendered_icon(self, size='24px'):
        """
        Retorna HTML do ícone renderizado.
        Prioridade: SVG > FontAwesome/Emoji > Emoji fallback por tipo.
        """
        if self.icon_svg:
            color = self.icon_color or '#6366F1'
            return f'<span style="display: inline-block; width: {size}; height: {size}; color: {color};">{self.icon_svg}</span>'
        if self.icon:
            if self.icon.startswith('fa-'):
                color = self.icon_color or '#6366F1'
                return f'<i class="{self.icon}" style="font-size: {size}; color: {color};"></i>'
            return f'<span style="font-size: {size};">{self.icon}</span>'
        return f'<span style="font-size: {size};">{self.default_icon_emoji}</span>'


class ActivityChain(AbstractBaseModel):
    """
    Template/definição de uma cadeia de atividades.
    
    Define a sequência de atividades que deve ser executada.
    Pode ser aplicada a qualquer Lead, Contact, etc.
    """
    APPLICABLE_MODEL_CHOICES = [
        ('lead', 'Lead'),
        ('contact', 'Contacto'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name='Chain Name',
        help_text='Ex: "Follow-up pós-reunião", "Onboarding novo cliente"'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    applicable_model = models.CharField(
        max_length=50,
        choices=APPLICABLE_MODEL_CHOICES,
        default='lead',
        verbose_name='Modelo',
        help_text='Qual o modelo a que esta cadeia se aplica (Lead, Contacto...)'
    )
    
    # Multi-company
    owner_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activity_chains',
        verbose_name='Owner Company'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Activity Chain'
        verbose_name_plural = 'Activity Chains'
    
    def __str__(self):
        return self.name
    
    @property
    def total_steps(self):
        return self.steps.count()


class ActivityChainStep(AbstractBaseModel):
    """
    Um passo dentro de uma cadeia de atividades.
    
    Liga um ActivityChain a uma ScheduledActivity (blueprint),
    definindo a ordem e o delay em relação ao passo anterior.
    
    Usage:
        step = ActivityChainStep.objects.create(
            chain=chain,
            activity=call_activity,
            order=1,
            delay_days=0,  # executa imediatamente
        )
    """
    chain = models.ForeignKey(
        ActivityChain,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name='Chain'
    )
    activity = models.ForeignKey(
        ScheduledActivity,
        on_delete=models.CASCADE,
        related_name='chain_steps',
        verbose_name='Activity Blueprint'
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name='Order',
        help_text='Ordem de execução dentro da cadeia (1, 2, 3...)'
    )
    delay_days = models.IntegerField(
        default=0,
        verbose_name='Delay (days)',
        help_text='Dias de espera após o passo anterior ser concluído (0 = executa logo)'
    )
    # Responsável padrão para este passo (pode ser sobrescrito na instância)
    default_assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chain_step_assignments',
        verbose_name='Default Assigned To'
    )
    # Em caso de insucesso: blueprint alternativo a executar antes de re-tentar este passo
    on_failure_activity = models.ForeignKey(
        ScheduledActivity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chain_steps_on_failure',
        verbose_name='Atividade se Insucesso',
        help_text='Blueprint a executar quando este passo falha (ex: "Não Atendeu"). Vazio = avança igualmente.'
    )
    on_failure_delay_days = models.IntegerField(
        default=1,
        verbose_name='Delay Insucesso (dias)',
        help_text='Dias de espera antes de executar a atividade de insucesso'
    )
    
    class Meta:
        ordering = ['chain', 'order']
        unique_together = [('chain', 'order')]
        verbose_name = 'Activity Chain Step'
        verbose_name_plural = 'Activity Chain Steps'
    
    def __str__(self):
        return f"{self.chain.name} - Step {self.order}: {self.activity.summary}"


class ActivityChainInstance(AbstractBaseModel):
    """
    Uma cadeia aplicada a um registo específico (Lead, Contact, etc.).
    
    Quando aplicas uma cadeia a um Lead, cria-se uma instância.
    Cada instância tem os seus próprios ActivityLogs independentes.
    
    Usage:
        instance = ActivityChainInstance.objects.create(
            chain=chain,
            content_object=lead,
            assigned_to=user,
            owner_company=company
        )
    """
    chain = models.ForeignKey(
        ActivityChain,
        on_delete=models.CASCADE,
        related_name='instances',
        verbose_name='Chain'
    )
    
    # GenericForeignKey - liga a qualquer modelo (Lead, Contact, etc.)
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.UUIDField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Status da instância
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('PAUSED', 'Paused'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='IN_PROGRESS',
        verbose_name='Status'
    )
    
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Started At'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Completed At'
    )
    
    # Responsável geral (pode ser sobrescrito por passo)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chain_instances',
        verbose_name='Assigned To'
    )
    
    # Multi-company
    owner_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chain_instances',
        verbose_name='Owner Company'
    )
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['status']),
        ]
        verbose_name = 'Activity Chain Instance'
        verbose_name_plural = 'Activity Chain Instances'
    
    def __str__(self):
        return f"{self.chain.name} - {self.status}"
    
    @property
    def current_step(self):
        """Retorna o passo atual (o próximo não concluído)"""
        completed_step_ids = self.logs.filter(
            result__isnull=False
        ).values_list('step_id', flat=True)
        return self.chain.steps.exclude(id__in=completed_step_ids).first()
    
    @property
    def progress_percentage(self):
        total = self.chain.total_steps
        if total == 0:
            return 0
        completed = self.logs.filter(result__isnull=False).count()
        return int((completed / total) * 100)


class ActivityLog(AbstractBaseModel):
    """
    Registo do resultado de um passo de cadeia numa instância específica.
    
    Cada vez que um utilizador conclui um passo da cadeia num Lead específico,
    cria-se um ActivityLog com o resultado e notas detalhadas.
    
    Este log é ÚNICO por instância + passo, garantindo rastreabilidade completa.
    
    Usage:
        log = ActivityLog.objects.create(
            chain_instance=instance,
            step=step,
            result='SUCCESS',
            notes='Cliente aceitou proposta, entrega em 1 semana',
            logged_by=user
        )
    """
    chain_instance = models.ForeignKey(
        ActivityChainInstance,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='Chain Instance'
    )
    step = models.ForeignKey(
        ActivityChainStep,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='Step'
    )
    
    # Data/hora em que foi executado
    executed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Executed At'
    )
    
    # Resultado
    RESULT_CHOICES = [
        ('SUCCESS', 'Sucesso'),
        ('FAILED', 'Falhado'),
        ('CALLBACK', 'Ligar mais tarde'),
        ('NO_ANSWER', 'Sem resposta'),
        ('NOT_INTERESTED', 'Não interessado'),
        ('PENDING', 'Pendente'),
    ]
    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        null=True,
        blank=True,
        verbose_name='Result'
    )
    
    # Notas detalhadas sobre o resultado
    notes = models.TextField(
        blank=True,
        verbose_name='Notes',
        help_text='Detalhes sobre o que aconteceu nesta atividade'
    )
    
    # Due date específica para este passo nesta instância (calculada pelo delay)
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Due Date'
    )
    due_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Due Time'
    )
    
    # Status do passo
    is_done = models.BooleanField(
        default=False,
        verbose_name='Is Done'
    )
    done_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Done At'
    )
    
    # Responsável para este passo desta instância
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs',
        verbose_name='Assigned To'
    )
    
    # Quem registou
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logged_activities',
        verbose_name='Logged By'
    )
    
    class Meta:
        ordering = ['chain_instance', 'step__order']
        indexes = [
            models.Index(fields=['chain_instance', 'step']),
            models.Index(fields=['is_done']),
            models.Index(fields=['due_date']),
        ]
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
    
    def __str__(self):
        return f"{self.step} - {self.result or 'Pending'}"
    
    @property
    def is_overdue(self):
        if self.is_done or not self.due_date:
            return False
        from django.utils import timezone
        return self.due_date < timezone.now().date()
    
    @property
    def is_today(self):
        if not self.due_date:
            return False
        from django.utils import timezone
        return self.due_date == timezone.now().date() and not self.is_done



class ActivityWorkflow(AbstractBaseModel):
    """
    Regras de automação para criar activities automaticamente.
    
    Define workflows do tipo: "Se CALL marcada como SUCCESS → criar EMAIL em +1 dia"
    
    Usage:
        # Criar workflow
        workflow = ActivityWorkflow.objects.create(
            name='Lead Nurturing - First Contact Success',
            model=ContentType.objects.get(app_label='crm', model='lead'),
            trigger_activity_type='CALL',
            trigger_result='SUCCESS',
            next_activity_template=email_template,
            delay_days=1
        )
    """
    from django.contrib.contenttypes.models import ContentType
    
    name = models.CharField(
        max_length=100,
        verbose_name='Workflow Name',
        help_text='Ex: "Lead Nurturing - First Contact Success"'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Explicação do workflow'
    )
    
    model = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        verbose_name='Model',
        help_text='Modelo que dispara este workflow (Lead, Sale, Purchase, etc.)'
    )
    
    trigger_activity_type = models.ForeignKey(
        'ActivityType',
        on_delete=models.PROTECT,
        verbose_name='Trigger Activity Type',
        help_text='Tipo de activity que dispara o workflow',
        null=True,
        blank=True,
    )
    
    trigger_result = models.CharField(
        max_length=20,
        choices=ActivityLog.RESULT_CHOICES,
        null=True,
        blank=True,
        verbose_name='Trigger Result',
        help_text='Resultado específico (ou None = qualquer resultado)'
    )
    
    trigger_condition = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Trigger Condition (Advanced)',
        help_text='Condições avançadas em JSON (futuro)'
    )
    
    next_activity_template = models.ForeignKey(
        'ScheduledActivity',
        on_delete=models.CASCADE,
        related_name='workflows',
        verbose_name='Next Activity Blueprint',
        help_text='Blueprint da próxima activity a criar'
    )
    
    delay_days = models.IntegerField(
        default=0,
        verbose_name='Delay (days)',
        help_text='Dias de espera antes de criar próxima activity'
    )
    
    # Odoo-style chaining configuration
    BASE_DATE_CHOICES = [
        ('DEADLINE', 'After Previous Activity Deadline'),
        ('COMPLETION', 'After Previous Activity Completion Date'),
    ]
    
    base_date_type = models.CharField(
        max_length=20,
        choices=BASE_DATE_CHOICES,
        default='COMPLETION',
        verbose_name='Base Date Type',
        help_text='Calcular próxima activity baseado em deadline (due_date) ou completion (done_date)'
    )
    
    CHAINING_MODE_CHOICES = [
        ('SUGGEST', 'Suggest Next Activity'),
        ('TRIGGER', 'Trigger Next Activity'),
    ]
    
    chaining_mode = models.CharField(
        max_length=20,
        choices=CHAINING_MODE_CHOICES,
        default='SUGGEST',
        verbose_name='Chaining Mode',
        help_text='SUGGEST = mostrar modal de confirmação | TRIGGER = criar automaticamente'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active',
        help_text='Desativar para pausar workflow sem deletar'
    )
    
    owner_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activity_workflows',
        verbose_name='Owner Company',
        help_text='NULL=global workflow, with value=private to company'
    )
    
    sequence = models.IntegerField(
        default=10,
        verbose_name='Sequence',
        help_text='Ordem de execução (menor = primeiro)'
    )
    
    class Meta:
        ordering = ['sequence', 'name']
        verbose_name = 'Activity Workflow'
        verbose_name_plural = 'Activity Workflows'
    
    def __str__(self):
        result_str = f" ({self.get_trigger_result_display()})" if self.trigger_result else ""
        type_name = self.trigger_activity_type.name if self.trigger_activity_type else 'Sem Tipo'
        return f"{self.name} - {type_name}{result_str}"
    
    def should_trigger(self, activity):
        """
        Verifica se este workflow deve disparar para a activity dada.
        
        Args:
            activity: ScheduledActivity instance
        
        Returns:
            bool
        """
        # Check: activity type match
        if activity.activity_type_id != self.trigger_activity_type_id:
            return False
        
        # Check: result match (se especificado)
        if self.trigger_result and activity.result != self.trigger_result:
            return False
        
        # Check: model match
        activity_model_ct = activity.content_type
        if activity_model_ct != self.model:
            return False
        
        # Check: is_active
        if not self.is_active:
            return False
        
        # TODO: Check advanced conditions (trigger_condition JSON)
        
        return True
    
    def execute(self, activity_log, user=None):
        """
        Executa workflow: cria próxima activity blueprint baseada no template.
        
        NOTA: Na nova arquitectura, este método recebe um ActivityLog (não ScheduledActivity).
        A lógica de scheduling passou para ActivityChain/ActivityChainInstance/ActivityLog.
        
        Args:
            activity_log: ActivityLog que disparou o workflow
            user: User que executou a atividade (opcional)
        
        Returns:
            ScheduledActivity blueprint criado OU None
        """
        # Criar blueprint usando template  
        # Nota: due_date e assigned_to agora ficam no ActivityLog, não no blueprint
        next_activity = self.next_activity_template.create_activity()
        
        return next_activity
    
    def get_suggested_activity_data(self, activity_log):
        """
        Retorna dados da próxima activity sugerida (para modo SUGGEST).
        
        Args:
            activity_log: ActivityLog que disparou
        
        Returns:
            dict com dados para criar activity
        """
        from datetime import timedelta
        from django.utils import timezone
        
        # Calcular due_date sugerida baseada no base_date_type e delay
        if self.base_date_type == 'DEADLINE' and activity_log.due_date:
            base_date = activity_log.due_date
        else:
            base_date = activity_log.done_at.date() if activity_log.done_at else timezone.now().date()
        
        due_date = base_date + timedelta(days=self.delay_days)
        
        return {
            'workflow': self,
            'template': self.next_activity_template,
            'assigned_to': activity_log.assigned_to,
            'due_date': due_date,
            'summary': self.next_activity_template.default_summary,
            'description': self.next_activity_template.default_description,
        }


class PlannedActivity(AbstractBaseModel):
    """
    Atividade planeada associada a qualquer modelo (Lead, Contacto, etc.).
    Exibida no chatter, estilo Odoo — permanece visível mesmo após concluída (log histórico).

    Usage:
        PlannedActivity.objects.create(
            content_object=lead,
            activity_type=ActivityType.objects.get(code='CALL'),
            summary='Ligar ao cliente',
            due_date=date.today() + timedelta(days=3),
            assigned_to=request.user,
            created_by=request.user,
        )
    """
    # GenericForeignKey — funciona com qualquer modelo
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        verbose_name='Content Type'
    )
    object_id = models.UUIDField(verbose_name='Object ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    # Tipo de atividade
    activity_type = models.ForeignKey(
        'ActivityType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planned_activities',
        verbose_name='Activity Type'
    )

    # Conteúdo
    summary = models.CharField(
        max_length=255,
        verbose_name='Summary',
        help_text='Título curto da atividade'
    )
    note = models.TextField(
        blank=True,
        verbose_name='Note',
        help_text='Nota opcional'
    )

    # Datas
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Due Date'
    )

    # Utilizadores
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planned_activities_assigned',
        verbose_name='Assigned To'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planned_activities_created',
        verbose_name='Created By'
    )

    # Estado
    STATUS_CHOICES = [
        ('PLANNED', 'Planeada'),
        ('DONE', 'Concluída'),
        ('CANCELLED', 'Cancelada'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED',
        verbose_name='Status'
    )
    done_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Done At'
    )
    done_note = models.TextField(
        blank=True,
        verbose_name='Done Note',
        help_text='Nota adicionada ao marcar como concluída'
    )

    class Meta:
        ordering = ['due_date', '-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['due_date']),
        ]
        verbose_name = 'Planned Activity'
        verbose_name_plural = 'Planned Activities'

    def __str__(self):
        return f"{self.summary} — {self.get_status_display()}"

    @property
    def days_until_due(self):
        """Retorna o número de dias até à data limite (negativo se atrasada)."""
        if not self.due_date:
            return None
        from django.utils import timezone
        delta = self.due_date - timezone.now().date()
        return delta.days

    @property
    def is_overdue(self):
        days = self.days_until_due
        return days is not None and days < 0 and self.status == 'PLANNED'

    @property
    def due_label(self):
        """Texto legível para o prazo (ex: 'Due in 3 days', 'Today', 'Overdue 2 days')."""
        days = self.days_until_due
        if days is None:
            return 'Sem prazo'
        if days == 0:
            return 'Hoje'
        if days > 0:
            return f'Em {days} dia{"s" if days != 1 else ""}'
        return f'Atrasada {abs(days)} dia{"s" if abs(days) != 1 else ""}'


# ─────────────────────────────────────────────────────────────────────────────
# NOTIFICATIONS
# ─────────────────────────────────────────────────────────────────────────────

class Notification(AbstractBaseModel):
    """
    Notificações internas do sistema.

    Exemplos:
    - João mencionou-te numa nota do Lead X
    - Lead Y foi atribuída a ti
    - Atividade Z está em atraso
    - Resposta de WhatsApp do Contacto W
    """

    NOTIFICATION_TYPES = [
        ('ACTIVITY_OVERDUE', 'Atividade em Atraso'),
        ('ACTIVITY_TODAY',   'Atividade para Hoje'),
        ('ACTIVITY_UPCOMING','Atividade Futura'),
        ('MENTION',          'Menção'),
        ('ASSIGNMENT',       'Atribuição'),
        ('WHATSAPP',         'WhatsApp'),
        ('EMAIL',            'Email'),
        ('STAGE_CHANGE',     'Mudança de Etapa'),
        ('COMMENT',          'Comentário'),
        ('SYSTEM',           'Sistema'),
    ]

    # Prioridade numérica para ordenação (menor = mais urgente)
    PRIORITY_MAP = {
        'ACTIVITY_OVERDUE': 1,
        'MENTION':          2,
        'ACTIVITY_TODAY':   3,
        'ASSIGNMENT':       4,
        'WHATSAPP':         5,
        'EMAIL':            5,
        'STAGE_CHANGE':     6,
        'COMMENT':          6,
        'ACTIVITY_UPCOMING':7,
        'SYSTEM':           8,
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Destinatário',
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        verbose_name='Tipo',
    )

    title   = models.CharField(max_length=255, verbose_name='Título')
    message = models.TextField(blank=True, verbose_name='Mensagem')
    link    = models.CharField(max_length=500, blank=True, verbose_name='Link')

    # Objeto relacionado (GenericFK opcional)
    related_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    related_object_id = models.UUIDField(null=True, blank=True)
    related_object    = GenericForeignKey('related_content_type', 'related_object_id')

    # Estado
    is_read = models.BooleanField(default=False, verbose_name='Lida')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Lida a')

    # Prioridade calculada (preenchida no save)
    priority = models.PositiveSmallIntegerField(default=99, verbose_name='Prioridade')

    # Urgente: True apenas para ACTIVITY_OVERDUE ou quando marcado explicitamente (e.g. menção urgente)
    is_urgent = models.BooleanField(default=False, verbose_name='Urgente')

    class Meta:
        ordering = ['priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'priority', '-created_at']),
        ]
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f"{self.user} — {self.title}"

    def save(self, *args, **kwargs):
        self.priority = self.PRIORITY_MAP.get(self.notification_type, 99)
        # Atividades em atraso são sempre urgentes
        if self.notification_type == 'ACTIVITY_OVERDUE':
            self.is_urgent = True
        super().save(*args, **kwargs)

    def mark_as_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
