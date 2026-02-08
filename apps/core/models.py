import uuid
from django.db import models
from django.conf import settings


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
