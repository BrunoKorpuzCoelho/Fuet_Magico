from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import AbstractBaseModel


class Contact(AbstractBaseModel):
    CONTACT_TYPE_CHOICES = [
        ('CLIENT', 'Client'),
        ('SUPPLIER', 'Supplier'),
        ('BOTH', 'Both'),
    ]
    
    CONTACT_CATEGORY_CHOICES = [
        ('PERSON', 'Person'),
        ('COMPANY', 'Company'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
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
    tags = models.JSONField(default=list, blank=True)
    
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
    
    def get_price_list(self):
        if hasattr(self, 'price_list') and self.price_list:
            return self.price_list
        
        if self.is_person and self.company:
            return self.company.get_price_list()
        
        return None
