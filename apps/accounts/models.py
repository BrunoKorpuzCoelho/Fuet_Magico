from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    EMPLOYEE = 'EMPLOYEE'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,20}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 20 digits allowed."
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True,
        null=True
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=EMPLOYEE
    )
    
    # Multi-company support
    companies = models.ManyToManyField(
        'core.Company',
        related_name='users',
        blank=True,
        verbose_name='Companies'
    )
    
    default_company = models.ForeignKey(
        'core.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_users',
        verbose_name='Default Company'
    )
    
    def get_full_name(self):
        full_name = super().get_full_name()
        return full_name if full_name else self.username
    
    def __str__(self):
        return self.username
