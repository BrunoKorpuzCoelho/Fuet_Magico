"""
Audit-log signals for WhatsAppTemplate.

Mirrors the approach used in apps/crm/signals.py for Lead:
  - pre_save  captures old field values
  - post_save compares old vs new and creates an AuditLog entry
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.core.models import AuditLog

# Temporary store for pre-save state (keyed by instance pk)
_template_pre_save_state: dict = {}

# Fields to track for change-detection
_TRACKED_FIELDS = [
    ('display_name', 'Nome', lambda x: x),
    ('name', 'Nome técnico', lambda x: x),
    ('category', 'Categoria', lambda x: x),
    ('language', 'Idioma', lambda x: x),
    ('status', 'Estado', lambda x: x),
    ('header_type', 'Tipo de cabeçalho', lambda x: x),
    ('header_text', 'Texto do cabeçalho', lambda x: x),
    ('body', 'Corpo', lambda x: (x[:100] + '…') if x and len(x) > 100 else x),
    ('footer', 'Rodapé', lambda x: x),
    ('buttons', 'Botões', lambda x: str(x) if x else None),
    ('variables', 'Variáveis', lambda x: str(x) if x else None),
    ('model_name', 'Modelo de dados', lambda x: x),
    ('allow_category_change', 'Permitir alt. categoria', lambda x: 'Sim' if x else 'Não'),
    ('is_active', 'Ativo', lambda x: 'Sim' if x else 'Não'),
    ('owner_company', 'Empresa', lambda x: str(x) if x else None),
    ('wa_template_uid', 'ID Meta', lambda x: x),
]


@receiver(pre_save, sender='whatsapp.WhatsAppTemplate')
def whatsapp_template_pre_save(sender, instance, **kwargs):
    """Capture template state before save to track changes."""
    if instance.pk:
        try:
            old = sender.objects.select_related('owner_company').get(pk=instance.pk)
            _template_pre_save_state[instance.pk] = {
                field_name: getattr(old, field_name)
                for field_name, _label, _fmt in _TRACKED_FIELDS
            }
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='whatsapp.WhatsAppTemplate')
def whatsapp_template_post_save(sender, instance, created, **kwargs):
    """Log WhatsAppTemplate creation and updates with detailed change tracking."""
    user = getattr(instance, '_current_user', None)

    if created:
        AuditLog.objects.create(
            user=user,
            action='CREATE',
            model_name='WhatsAppTemplate',
            object_id=str(instance.pk),
            details={
                'display_name': instance.display_name,
                'name': instance.name,
                'category': instance.category,
                'language': instance.language,
                'status': instance.status,
                'owner_company': str(instance.owner_company) if instance.owner_company else None,
            },
        )
        return

    # --- UPDATE ---
    old_state = _template_pre_save_state.pop(instance.pk, None)
    if not old_state:
        return

    changes = {}
    for field_name, _label, formatter in _TRACKED_FIELDS:
        old_val = old_state.get(field_name)
        new_val = getattr(instance, field_name)
        if old_val != new_val:
            changes[field_name] = {
                'old': formatter(old_val),
                'new': formatter(new_val),
            }

    if changes:
        AuditLog.objects.create(
            user=user,
            action='UPDATE',
            model_name='WhatsAppTemplate',
            object_id=str(instance.pk),
            details={
                'display_name': instance.display_name,
                'changes': changes,
            },
        )
