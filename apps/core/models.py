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
