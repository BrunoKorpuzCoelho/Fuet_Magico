from django.db import models
from django.conf import settings
from django.utils import timezone


class UserSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    dark_mode = models.BooleanField(default=True)
    developer_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Settings for {self.user.username}"


class Notification(models.Model):
    
    NOTIFICATION_TYPES = [
        ('ORDER', 'Nova Encomenda'),
        ('PAYMENT', 'Pagamento'),
        ('STOCK', 'Stock'),
        ('SYSTEM', 'Sistema'),
        ('MESSAGE', 'Mensagem'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='SYSTEM'
    )
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @classmethod
    def get_unread_count(cls, user):
        return cls.objects.filter(user=user, is_read=False).count()
