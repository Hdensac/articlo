from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from notifications.models import Notification
from users.models import User

@receiver(post_save, sender=Order)
def create_order_notifications(sender, instance, created, **kwargs):
    if created:
        # Notification pour le vendeur
        Notification.objects.create(
            recipient=instance.seller,
            title="Nouvelle commande reçue",
            message=f"Vous avez reçu une nouvelle commande pour l'article : {instance.article.title}.",
        )
        # Notification pour l'admin
        admin_users = User.objects.filter(role='admin')
        for admin in admin_users:
            Notification.objects.create(
                recipient=admin,
                title="Nouvelle commande sur le site",
                message=f"Une nouvelle commande a été passée pour l'article : {instance.article.title} par {instance.client_name}.",
            )
