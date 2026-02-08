from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import AbstractBaseModel


class ContactTag(AbstractBaseModel):
    """
    Model for contact tags that can be reused across multiple contacts.
    Only name is required. Color is optional with golden default.
    
    Multi-Company Support:
    - If owner_company is NULL: Tag is GLOBAL (all companies can use)
    - If owner_company has value: Tag is PRIVATE (only that company can use)
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='Tag Name')
    color = models.CharField(max_length=7, default='#dbc693', verbose_name='Tag Color')
    
    # Multi-company support: NULL = global, with value = private to that company
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contact_tags',
        verbose_name='Owner Company',
        help_text='Leave empty for global tags (all companies). Set to make tag private to specific company.'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Contact Tag'
        verbose_name_plural = 'Contact Tags'
    
    def __str__(self):
        return self.name


class Contact(AbstractBaseModel):
    CONTACT_TYPE_CHOICES = [
        ('CLIENT', 'Client'),
        ('SUPPLIER', 'Supplier'),
        ('BOTH', 'Both'),
    ]
    
    CONTACT_CATEGORY_CHOICES = [
        ('PERSON', 'Person'),
        ('COMPANY', 'Company'),
        ('BILLING', 'Billing'),
        ('SHIPPING', 'Shipping'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True, verbose_name='District')
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, default='Portugal')
    website = models.URLField(max_length=255, blank=True, verbose_name='Website')
    language = models.CharField(max_length=10, blank=True, default='pt_PT', verbose_name='Language')
    nif = models.CharField(max_length=20, blank=True, verbose_name='NIF/Tax ID')
    notes = models.TextField(blank=True)
    
    contact_type = models.CharField(
        max_length=10,
        choices=CONTACT_TYPE_CHOICES,
        default='CLIENT'
    )
    
    contact_category = models.CharField(
        max_length=10,
        choices=CONTACT_CATEGORY_CHOICES,
        default='PERSON'
    )
    
    company = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        limit_choices_to={'contact_category': 'COMPANY'}
    )
    
    position = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(ContactTag, blank=True, related_name='contacts')
    
    # Multi-company support: NULL = global, with value = private to that company
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contacts',
        verbose_name='Owner Company',
        help_text='Leave empty for global contacts (all companies). Set to make contact private to specific company.'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
    
    def __str__(self):
        if self.contact_category == 'PERSON' and self.company:
            return f"{self.name} ({self.company.name})"
        return self.name
    
    def clean(self):
        super().clean()
        
        if self.contact_category == 'COMPANY' and self.company:
            raise ValidationError({
                'company': 'A company cannot be associated with another company.'
            })
        
        if self.company and self.company.contact_category != 'COMPANY':
            raise ValidationError({
                'company': 'A person can only be associated with a company, not another person.'
            })
        
        if self.contact_category == 'COMPANY' and self.position:
            raise ValidationError({
                'position': 'Position field is only for persons, not companies.'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_company(self):
        return self.contact_category == 'COMPANY'
    
    @property
    def is_person(self):
        return self.contact_category == 'PERSON'
    
    def get_avatar_url(self):
        """Retorna URL do avatar (upload ou default baseado em categoria/tipo)"""
        # TODO: Adicionar campo avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
        # if hasattr(self, 'avatar') and self.avatar:
        #     return self.avatar.url
        
        # Default baseado na categoria (prioridade)
        if self.contact_category == 'PERSON':
            return '/static/images/avatars/defaults/default-person.svg'
        elif self.contact_category == 'COMPANY':
            return '/static/images/avatars/defaults/default-company.svg'
        elif self.contact_category == 'BILLING':
            return '/static/images/avatars/defaults/default-billing.svg'
        elif self.contact_category == 'SHIPPING':
            return '/static/images/avatars/defaults/default-shipping.svg'
        elif self.contact_category == 'OTHER':
            return '/static/images/avatars/defaults/default-other.svg'
        
        # Fallback genérico
        return '/static/images/avatars/defaults/default-other.svg'
    
    def get_price_list(self):
        if hasattr(self, 'price_list') and self.price_list:
            return self.price_list
        
        if self.is_person and self.company:
            return self.company.get_price_list()
        
        return None
