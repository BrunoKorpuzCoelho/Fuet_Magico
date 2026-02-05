from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog

User = get_user_model()


@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    AuditLog.objects.create(
        user=instance if not created else None,
        action=action,
        model_name=sender.__name__,
        object_id=str(instance.pk),
        details={
            'username': instance.username,
            'email': instance.email,
            'role': instance.role,
        }
    )


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=None,
        action='DELETE',
        model_name=sender.__name__,
        object_id=str(instance.pk),
        details={
            'username': instance.username,
            'email': instance.email,
        }
    )
