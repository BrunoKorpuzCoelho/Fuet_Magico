from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from apps.core.models import AbstractBaseModel, Company
from apps.contacts.models import Contact

User = get_user_model()


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
        ('OTHER', 'Other'),
    ]
    
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Contact'
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
    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Tags',
        help_text='Tag system same as Contacts (list of dicts with name+color)'
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

