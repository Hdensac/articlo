from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('seller', 'Vendeur'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro WhatsApp pour les vendeurs")

    # Fix related_name conflicts with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_seller(self):
        """Vérifie si l'utilisateur est un vendeur"""
        return self.role == 'seller'

    def is_client(self):
        """Vérifie si l'utilisateur est un client"""
        return self.role == 'client'

    def is_admin(self):
        """Vérifie si l'utilisateur est un admin"""
        return self.role == 'admin'

    def can_order(self):
        """Vérifie si l'utilisateur peut passer des commandes"""
        return not self.is_seller()

# Create your models here.
