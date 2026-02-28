from django.db.models.signals import post_migrate, post_save, pre_save
from django.dispatch import receiver
from apps.core.models import AuditLog


@receiver(post_migrate)
def create_default_crm_stages(sender, **kwargs):
    """
    Cria estágios CRM default após migrations.
    Só cria se não existirem NENHUNS estágios (globais ou de empresa).
    """
    if sender.name != 'apps.crm':
        return
    
    from .models import CRMStage
    
    # Se já existem estágios (globais OU de empresa), não criar
    if CRMStage.objects.exists():
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


# Store original Lead state before save
_lead_pre_save_state = {}


# ─── Pontuação Preditiva — auto-probability on stage change ──────────────────

@receiver(pre_save, sender='crm.Lead')
def lead_capture_previous_stage(sender, instance, **kwargs):
    """Guarda o stage anterior para detectar mudança de stage."""
    if instance.pk:
        try:
            old = sender.objects.only('stage_id').get(pk=instance.pk)
            instance._previous_stage_id = old.stage_id
        except sender.DoesNotExist:
            instance._previous_stage_id = None
    else:
        instance._previous_stage_id = None


@receiver(post_save, sender='crm.Lead')
def lead_auto_probability(sender, instance, created, **kwargs):
    """
    Quando o estágio de uma lead muda (ou é criada), aplica automaticamente
    a probabilidade histórica do novo estágio — se predictive_scoring estiver ativo.
    Não dispara se probability_locked=True.
    """
    from .services import apply_stage_probability_to_lead

    prev_stage_id = getattr(instance, '_previous_stage_id', None)
    stage_changed = created or (prev_stage_id != instance.stage_id)

    if not stage_changed:
        return
    if instance.probability_locked:
        return

    old_probability = instance.probability
    apply_stage_probability_to_lead(instance)

    if instance.probability != old_probability:
        # Salva só o campo probability, sem disparar signals novamente
        sender.objects.filter(pk=instance.pk).update(probability=instance.probability)


# ─── Audit log signals ───────────────────────────────────────────────────────

@receiver(pre_save, sender='crm.Lead')
def lead_pre_save(sender, instance, **kwargs):
    """
    Capture Lead state before save to track changes.
    """
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _lead_pre_save_state[instance.pk] = {
                'contact': old_instance.contact,
                'contact_name': old_instance.contact_name,
                'email_from': old_instance.email_from,
                'phone': old_instance.phone,
                'title': old_instance.title,
                'description': old_instance.description,
                'estimated_value': old_instance.estimated_value,
                'probability': old_instance.probability,
                'priority': old_instance.priority,
                'stage': old_instance.stage,
                'source': old_instance.source,
                'expected_close_date': old_instance.expected_close_date,
                'assigned_to': old_instance.assigned_to,
                'lost_reason': old_instance.lost_reason,
            }
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='crm.Lead')
def lead_post_save(sender, instance, created, **kwargs):
    """
    Log Lead creation and updates with detailed change tracking.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get the current user from the request context (if available)
    # This will be set by the view when saving
    user = getattr(instance, '_current_user', None)
    
    if created:
        # Log creation
        AuditLog.objects.create(
            user=user,
            action='CREATE',
            model_name='Lead',
            object_id=str(instance.pk),
            details={
                'title': instance.title,
                'contact': str(instance.contact) if instance.contact else None,
                'stage': str(instance.stage),
                'assigned_to': str(instance.assigned_to) if instance.assigned_to else None,
                'estimated_value': str(instance.estimated_value),
            }
        )
    else:
        # Log updates with change tracking
        old_state = _lead_pre_save_state.get(instance.pk, {})
        if old_state:
            changes = {}
            
            # Track all field changes
            fields_to_track = [
                ('contact', lambda x: str(x) if x else None),
                ('contact_name', lambda x: x),
                ('email_from', lambda x: x),
                ('phone', lambda x: x),
                ('title', lambda x: x),
                ('description', lambda x: x[:100] + '...' if x and len(x) > 100 else x),
                ('estimated_value', lambda x: str(x)),
                ('probability', lambda x: str(x)),
                ('priority', lambda x: x),
                ('stage', lambda x: str(x)),
                ('source', lambda x: x),
                ('expected_close_date', lambda x: str(x) if x else None),
                ('assigned_to', lambda x: str(x) if x else None),
                ('lost_reason', lambda x: x[:100] + '...' if x and len(x) > 100 else x),
            ]
            
            for field_name, formatter in fields_to_track:
                old_value = old_state.get(field_name)
                new_value = getattr(instance, field_name)
                
                if old_value != new_value:
                    changes[field_name] = {
                        'old': formatter(old_value),
                        'new': formatter(new_value),
                    }
            
            # Only create log entry if there were actual changes
            if changes:
                AuditLog.objects.create(
                    user=user,
                    action='UPDATE',
                    model_name='Lead',
                    object_id=str(instance.pk),
                    details={
                        'title': instance.title,
                        'changes': changes,
                    }
                )
            
            # Clean up stored state
            _lead_pre_save_state.pop(instance.pk, None)
