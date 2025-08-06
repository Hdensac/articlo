from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from articles.models import Article
from notifications.models import Notification
from users.models import User
from .models import Order
from .forms import OrderForm, OrderStatusForm


def order_article(request, article_id):
    """Vue pour commander un article"""
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.article = article
            order.seller = article.seller
            order.save()

            # Créer des notifications
            create_order_notifications(order)

            messages.success(
                request,
                f'Votre commande pour "{article.title}" a été envoyée avec succès ! '
                f'Le vendeur va vous contacter bientôt.'
            )
            return redirect('orders:success', order_id=order.id)
    else:
        form = OrderForm()

    context = {
        'form': form,
        'article': article,
        'page_title': f'Commander "{article.title}"'
    }
    return render(request, 'orders/order_form.html', context)


def order_success(request, order_id):
    """Page de confirmation de commande"""
    order = get_object_or_404(Order, id=order_id)

    context = {
        'order': order,
        'page_title': 'Commande confirmée'
    }
    return render(request, 'orders/order_success.html', context)


@login_required
def order_detail(request, order_id):
    """Vue pour voir le détail d'une commande (vendeur seulement)"""
    order = get_object_or_404(Order, id=order_id)

    # Vérifier que l'utilisateur est le vendeur de cette commande
    if order.seller != request.user:
        raise Http404("Commande non trouvée")

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            old_status = order.status
            form.save()

            # Créer une notification si le statut a changé
            if old_status != order.status:
                create_status_change_notification(order, old_status)

            messages.success(
                request,
                f'Le statut de la commande a été mis à jour : {order.get_status_display()}'
            )
            return redirect('seller_dashboard')
    else:
        form = OrderStatusForm(instance=order)

    context = {
        'order': order,
        'form': form,
        'page_title': f'Commande #{order.id}'
    }
    return render(request, 'orders/order_detail.html', context)


def create_order_notifications(order):
    """Créer les notifications pour une nouvelle commande"""
    # Notification pour le vendeur
    Notification.objects.create(
        recipient=order.seller,
        title="Nouvelle commande reçue !",
        message=f"{order.client_name} souhaite commander votre article '{order.article.title}' "
                f"au prix de {order.article.price}€. "
                f"Contactez-le au {order.client_phone}."
    )

    # Notification pour les administrateurs
    admins = User.objects.filter(role='admin')
    for admin in admins:
        Notification.objects.create(
            recipient=admin,
            title="Nouvelle commande sur la plateforme",
            message=f"Commande #{order.id} : {order.client_name} a commandé "
                    f"'{order.article.title}' chez {order.seller.username}."
        )


def create_status_change_notification(order, old_status):
    """Créer une notification lors du changement de statut"""
    status_messages = {
        'confirmed': f"Bonne nouvelle ! Votre commande pour '{order.article.title}' a été confirmée par le vendeur.",
        'cancelled': f"Votre commande pour '{order.article.title}' a été annulée par le vendeur."
    }

    if order.status in status_messages:
        # Note: Ici on pourrait envoyer un email au client
        # Pour l'instant, on crée juste une notification pour l'admin
        admins = User.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                title=f"Commande #{order.id} - Statut mis à jour",
                message=f"Le vendeur {order.seller.username} a changé le statut de "
                        f"'{old_status}' vers '{order.status}' pour la commande de {order.client_name}."
            )
