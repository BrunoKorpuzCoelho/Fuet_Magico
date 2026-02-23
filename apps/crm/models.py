from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from apps.core.models import AbstractBaseModel, Company
from apps.contacts.models import Contact

User = get_user_model()


class CRMTag(AbstractBaseModel):
    """
    Modelo para tags de CRM reutilizáveis em múltiplos leads/oportunidades.
    Replicação do ContactTag para o módulo CRM.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='Tag Name')
    color = models.CharField(max_length=7, default='#dbc693', verbose_name='Tag Color')
    
    owner_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='crm_tags',
        verbose_name='Owner Company',
        help_text='Leave empty for global tags. Set to make tag private to specific company.'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'CRM Tag'
        verbose_name_plural = 'CRM Tags'
    
    def __str__(self):
        return self.name


class CRMStage(AbstractBaseModel):
    """
    Modelo para estágios personalizáveis do pipeline CRM.
    Equivalente ao Odoo CRM stages - permite criar e configurar stages customizados.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nome do Estágio',
        help_text='Ex: New, Qualified, Proposition, Won'
    )
    sequence = models.IntegerField(
        default=10,
        verbose_name='Ordem',
        help_text='Ordem de exibição no pipeline (menor = primeiro)'
    )
    is_won_stage = models.BooleanField(
        default=False,
        verbose_name='Estágio de Vitória',
        help_text='Marca este estágio como ganho/venda concluída'
    )
    is_lost_stage = models.BooleanField(
        default=False,
        verbose_name='Estágio de Perda',
        help_text='Marca este estágio como perdido/oportunidade falhada'
    )
    fold_by_default = models.BooleanField(
        default=False,
        verbose_name='Colapsado por Padrão',
        help_text='Se deve aparecer colapsado no kanban'
    )
    routing_in_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Dias de Roteamento',
        help_text='Dias sem update para highlight (0=desativado). Usado para progress bar colorido.'
    )
    color = models.CharField(
        max_length=7,
        default='#6c757d',
        verbose_name='Cor',
        help_text='Cor hexadecimal (ex: #28a745 para verde)'
    )
    win_probability = models.FloatField(
        default=10.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Probabilidade Histórica (%)',
        help_text='Calculado automaticamente: % de leads ganhas que passaram por este estágio'
    )
    owner_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='crm_stages',
        verbose_name='Empresa',
        help_text='NULL=global/shared, com valor=privado da empresa'
    )
    
    class Meta:
        ordering = ['sequence', 'name']
        verbose_name = 'Estágio CRM'
        verbose_name_plural = 'Estágios CRM'
        unique_together = [['name', 'owner_company']]
    
    def __str__(self):
        return self.name
    
    def filter_by_company(self, company=None):
        """
        Filtra stages por empresa.
        Retorna stages globais (owner_company=NULL) + stages da empresa específica.
        """
        if company:
            return CRMStage.objects.filter(
                models.Q(owner_company__isnull=True) | models.Q(owner_company=company),
                is_active=True
            )
        return CRMStage.objects.filter(owner_company__isnull=True, is_active=True)


class Lead(AbstractBaseModel):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    SOURCE_CHOICES = [
        ('WEBSITE', 'Website'),
        ('REFERRAL', 'Referral'),
        ('COLD_CALL', 'Cold Call'),
        ('SOCIAL_MEDIA', 'Social Media'),
        ('RETURNING', 'Cliente Recorrente'),
        ('OTHER', 'Other'),
    ]

    LOST_REASON_CATEGORY_CHOICES = [
        ('PRICE', 'Preço'),
        ('COMPETITOR', 'Concorrência'),
        ('TIMING', 'Timing / Sem urgência'),
        ('NO_BUDGET', 'Sem Orçamento'),
        ('NO_RESPONSE', 'Sem Resposta'),
        ('REQUIREMENTS', 'Requisitos não cumpridos'),
        ('OTHER', 'Outro'),
    ]

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Contact'
    )
    contact_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Contact Name',
        help_text='Nome do contacto (preenchido automaticamente se selecionar contacto)'
    )
    email_from = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name='Email',
        help_text='Email do contacto da oportunidade'
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Phone',
        help_text='Telefone do contacto da oportunidade'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Opportunity Title'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Detailed Description'
    )
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        blank=True,  # Permite vazio no form
        verbose_name='Expected Revenue'
    )
    probability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=10,
        verbose_name='Probability (%)',
        help_text='Probability of closing (0-100%)'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name='Priority'
    )
    stage = models.ForeignKey(
        CRMStage,
        on_delete=models.PROTECT,
        related_name='leads',
        verbose_name='Stage'
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='OTHER',
        verbose_name='Source'
    )
    expected_close_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Expected Close Date'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads',
        verbose_name='Assigned To'
    )
    lost_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='Lost Reason',
        help_text='Required if stage is Lost'
    )
    tags = models.ManyToManyField(
        CRMTag,
        blank=True,
        related_name='leads',
        verbose_name='Tags'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notes',
        help_text='Rich text notes (HTML formatted)'
    )
    owner_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Owner Company',
        help_text='NULL=global, with value=private to company'
    )
    stage_updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Stage Updated At',
        help_text='Timestamp when stage was last changed (for routing calculation)'
    )
    is_prospect = models.BooleanField(
        default=False,
        verbose_name='É Prospecto',
        help_text='Prospecto ainda n\u00e3o qualificado — n\u00e3o aparece no pipeline principal'
    )
    probability_locked = models.BooleanField(
        default=False,
        verbose_name='Probabilidade Manual',
        help_text='Se True, a probabilidade não é atualizada automaticamente pelo sistema'
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Fecho',
        help_text='Data/hora em que a lead foi ganha ou perdida. Preenchido automaticamente.'
    )
    lost_reason_category = models.CharField(
        max_length=20,
        choices=LOST_REASON_CATEGORY_CHOICES,
        blank=True,
        default='',
        verbose_name='Categoria do Motivo de Perda',
        help_text='Categoria estruturada do motivo de perda (para análise em relatórios)'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
    
    def __str__(self):
        if self.contact:
            return f"{self.title} - {self.contact.name}"
        return self.title
    
    @property
    def priority_stars(self):
        priority_map = {
            'LOW': 1,
            'MEDIUM': 2,
            'HIGH': 3,
        }
        return priority_map.get(self.priority, 2)
    
    def save(self, *args, **kwargs):
        """Override: auto-set closed_at when stage changes to won/lost; clear it when moved back."""
        if self.pk and self.stage_id:
            try:
                old = Lead.objects.only('stage_id', 'closed_at').get(pk=self.pk)
                if old.stage_id != self.stage_id:
                    self.stage_updated_at = timezone.now()
                    if self.stage.is_won_stage or self.stage.is_lost_stage:
                        if not self.closed_at:
                            self.closed_at = timezone.now()
                    else:
                        self.closed_at = None
            except Lead.DoesNotExist:
                pass
        elif not self.pk and self.stage_id:
            # New lead — set closed_at if created directly in a won/lost stage
            try:
                if self.stage.is_won_stage or self.stage.is_lost_stage:
                    if not self.closed_at:
                        self.closed_at = timezone.now()
            except Exception:
                pass
        super().save(*args, **kwargs)

    def filter_by_company(self, company=None):
        if company:
            return Lead.objects.filter(
                models.Q(owner_company__isnull=True) | models.Q(owner_company=company),
                is_active=True
            )
        return Lead.objects.filter(owner_company__isnull=True, is_active=True)


class Activity(AbstractBaseModel):
    ACTIVITY_TYPE_CHOICES = [
        ('TODO', 'To-Do'),
        ('EMAIL', 'Email'),
        ('CALL', 'Call'),
        ('WHATSAPP', 'WhatsApp'),
        ('DOCUMENT', 'Document'),
        ('SIGNATURE', 'Signature'),
    ]
    
    lead = models.ForeignKey(
        'Lead',
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='Lead'
    )
    # Blueprint referenciado (nullable — atividades ad-hoc não têm blueprint)
    scheduled_activity = models.ForeignKey(
        'core.ScheduledActivity',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='crm_activities',
        verbose_name='Atividade Programada',
        help_text='Blueprint que originou esta atividade (opcional)'
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        verbose_name='Activity Type'
    )
    summary = models.CharField(
        max_length=255,
        verbose_name='Summary'
    )
    due_date = models.DateField(
        verbose_name='Due Date'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_activities',
        verbose_name='Assigned To'
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name='Is Done'
    )
    done_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Done Date',
        help_text='Timestamp when activity was marked as done'
    )
    feedback = models.TextField(
        default='',
        blank=True,
        verbose_name='Feedback',
        help_text='Note when marking as done (required)'
    )
    owner_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activities',
        verbose_name='Owner Company',
        help_text='NULL=global, with value=private to company'
    )
    
    class Meta:
        ordering = ['due_date', '-created_at']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return self.summary
    
    @property
    def is_overdue(self):
        if self.is_done:
            return False
        return date.today() > self.due_date
    
    @property
    def status_color(self):
        if self.is_done:
            return 'green'
        if self.is_overdue:
            return 'red'
        if date.today() == self.due_date:
            return 'yellow'
        return 'green'
    
    def save(self, *args, **kwargs):
        if self.is_done and not self.done_date:
            self.done_date = timezone.now()
        super().save(*args, **kwargs)


class LeadNote(AbstractBaseModel):
    """
    Nota interna no chatter de um Lead.
    Visível apenas pelos utilizadores do ERP — não é enviada ao cliente.
    Suporta menções via @username que geram notificações MENTION.
    """
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='chatter_notes',
        verbose_name='Lead',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='lead_notes',
        verbose_name='Autor',
    )
    content = models.TextField(verbose_name='Conteúdo')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Nota do Lead'
        verbose_name_plural = 'Notas do Lead'

    def __str__(self):
        return f'{self.author} — {self.lead} ({self.created_at:%d/%m/%Y})'


class CRMConfig(AbstractBaseModel):
    """
    Configura\u00e7\u00f5es de CRM por empresa.
    Criado automaticamente na primeira vez que as defini\u00e7\u00f5es s\u00e3o guardadas.
    """
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name='crm_config',
        verbose_name='Empresa'
    )
    predictive_scoring = models.BooleanField(
        default=True,
        verbose_name='Pontua\u00e7\u00e3o Preditiva',
        help_text='Calcula automaticamente a probabilidade de fecho com base no hist\u00f3rico de leads'
    )
    prospects_enabled = models.BooleanField(
        default=False,
        verbose_name='Prospectos',
        help_text='Ativa a fase de prospecto antes do pipeline (leads n\u00e3o qualificadas)'
    )
    lead_generation_years = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Per\u00edodo Hist\u00f3rico (anos)',
        help_text='Quantos anos de hist\u00f3rico usar para gerar leads autom\u00e1ticas'
    )
    last_probability_update = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='\u00daltima Atualiza\u00e7\u00e3o de Probabilidades'
    )

    class Meta:
        verbose_name = 'Configura\u00e7\u00f5es CRM'
        verbose_name_plural = 'Configura\u00e7\u00f5es CRM'

    def __str__(self):
        return f'CRM Config — {self.company}'

    @classmethod
    def for_company(cls, company):
        """Retorna (ou cria) a config CRM da empresa."""
        config, _ = cls.objects.get_or_create(company=company)
        return config


# Os emails enviados/recebidos no contexto de uma lead s\u00e3o guardados em
# apps.core.models.ChatterMessage (message_type='EMAIL') com GenericForeignKey
# a apontar para o registo em questão (Lead, futuramente Compra, Venda, etc.).
#
# Para consultar emails de uma lead:
#   from django.contrib.contenttypes.models import ContentType
#   from apps.core.models import ChatterMessage
#   ct = ContentType.objects.get_for_model(Lead)
#   emails = ChatterMessage.objects.filter(
#       content_type=ct, object_id=lead.id, message_type='EMAIL'
#   )
