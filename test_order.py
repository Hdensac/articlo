#!/usr/bin/env python
"""
Script pour tester le système de commande
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from articles.models import Article
from orders.models import Order
from notifications.models import Notification
from users.models import User

def test_order_system():
    print("🧪 Test du système de commande...")
    
    # Récupérer un article existant
    try:
        article = Article.objects.first()
        if not article:
            print("❌ Aucun article trouvé. Exécutez d'abord create_test_data.py")
            return
        
        print(f"📦 Article sélectionné: {article.title} ({article.price}€)")
        print(f"👤 Vendeur: {article.seller.username}")
        
        # Créer une commande de test
        order = Order.objects.create(
            article=article,
            seller=article.seller,
            client_name="Jean Dupont",
            client_phone="+33123456789",
            client_email="jean.dupont@test.com",
            message="Bonjour, je suis intéressé par cet article. Est-il toujours disponible ?"
        )
        
        print(f"✅ Commande créée: #{order.id}")
        print(f"📅 Date: {order.created_at}")
        print(f"📱 Client: {order.client_name} ({order.client_phone})")
        
        # Vérifier les notifications
        notifications_vendeur = Notification.objects.filter(
            recipient=article.seller
        ).count()
        
        notifications_admin = Notification.objects.filter(
            recipient__role='admin'
        ).count()
        
        print(f"🔔 Notifications vendeur: {notifications_vendeur}")
        print(f"🔔 Notifications admin: {notifications_admin}")
        
        # Statistiques
        total_orders = Order.objects.count()
        total_notifications = Notification.objects.count()
        
        print(f"\n📊 Statistiques:")
        print(f"   - Total commandes: {total_orders}")
        print(f"   - Total notifications: {total_notifications}")
        print(f"   - Articles disponibles: {Article.objects.count()}")
        print(f"   - Vendeurs actifs: {User.objects.filter(role='seller').count()}")
        
        print(f"\n🌐 URLs de test:")
        print(f"   - Commande: http://127.0.0.1:8000/orders/article/{article.id}/order/")
        print(f"   - Détail commande: http://127.0.0.1:8000/orders/{order.id}/")
        print(f"   - Article: http://127.0.0.1:8000/articles/{article.id}/")
        
        print(f"\n🎉 Test du système de commande réussi !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == '__main__':
    test_order_system()
