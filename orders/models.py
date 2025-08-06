from django.db import models

from articles.models import Article
from users.models import User

class Order(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='orders')
    client_name = models.CharField(max_length=255)
    client_phone = models.CharField(max_length=20)
    client_email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Commande de {self.client_name} pour {self.article.title}"
