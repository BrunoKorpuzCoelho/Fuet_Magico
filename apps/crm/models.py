from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import AbstractBaseModel, Company


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

