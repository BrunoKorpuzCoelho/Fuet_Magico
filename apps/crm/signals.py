from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_crm_stages(sender, **kwargs):
    """
    Cria estágios CRM default após migrations.
    Só cria se não existirem estágios globais (owner_company=None).
    """
    if sender.name != 'apps.crm':
        return
    
    from .models import CRMStage
    
    # Verificar se já existem estágios globais
    if CRMStage.objects.filter(owner_company__isnull=True).exists():
        return
    
    # Criar estágios default
    default_stages = [
        {
            'name': 'New',
            'sequence': 1,
            'color': '#6c757d',
            'routing_in_days': 7,
            'is_won_stage': False,
            'fold_by_default': False,
        },
        {
            'name': 'Qualified',
            'sequence': 2,
            'color': '#17a2b8',
            'routing_in_days': 0,
            'is_won_stage': False,
            'fold_by_default': False,
        },
        {
            'name': 'Proposition',
            'sequence': 3,
            'color': '#ffc107',
            'routing_in_days': 0,
            'is_won_stage': False,
            'fold_by_default': False,
        },
        {
            'name': 'Won',
            'sequence': 4,
            'color': '#28a745',
            'routing_in_days': 0,
            'is_won_stage': True,
            'fold_by_default': True,
        },
        {
            'name': 'Lost',
            'sequence': 5,
            'color': '#dc3545',
            'routing_in_days': 0,
            'is_won_stage': False,
            'fold_by_default': True,
        },
    ]
    
    for stage_data in default_stages:
        CRMStage.objects.create(**stage_data)
    
    print(f"✅ Created {len(default_stages)} default CRM stages")
