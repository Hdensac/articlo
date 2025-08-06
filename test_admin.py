#!/usr/bin/env python
"""
Script pour tester le dashboard admin
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from articles.models import Article
from orders.models import Order
from notifications.models import Notification

def test_admin_dashboard():
    print("👑 Test du dashboard admin...")
    
    # Vérifier s'il y a un admin
    admin_users = User.objects.filter(role='admin')
    if not admin_users.exists():
        print("⚠️  Aucun administrateur trouvé. Création d'un admin de test...")
        
        # Créer un admin de test
        admin = User.objects.create_user(
            username='admin',
            email='admin@articlo.com',
            password='admin123',
            role='admin',
            first_name='Admin',
            last_name='Articlo'
        )
        print(f"✅ Admin créé: {admin.username} (mot de passe: admin123)")
    else:
        admin = admin_users.first()
        print(f"✅ Admin trouvé: {admin.username}")
    
    # Statistiques pour le dashboard
    stats = {
        'total_users': User.objects.count(),
        'total_sellers': User.objects.filter(role='seller').count(),
        'total_clients': User.objects.filter(role='client').count(),
        'total_articles': Article.objects.count(),
        'total_orders': Order.objects.count(),
        'orders_pending': Order.objects.filter(status='pending').count(),
        'orders_confirmed': Order.objects.filter(status='confirmed').count(),
        'orders_cancelled': Order.objects.filter(status='cancelled').count(),
        'unread_notifications': Notification.objects.filter(is_read=False).count(),
    }
    
    print(f"\n📊 Statistiques de la plateforme:")
    print(f"   - Utilisateurs totaux: {stats['total_users']}")
    print(f"     • Vendeurs: {stats['total_sellers']}")
    print(f"     • Clients: {stats['total_clients']}")
    print(f"     • Autres: {stats['total_users'] - stats['total_sellers'] - stats['total_clients']}")
    print(f"   - Articles: {stats['total_articles']}")
    print(f"   - Commandes: {stats['total_orders']}")
    print(f"     • En attente: {stats['orders_pending']}")
    print(f"     • Confirmées: {stats['orders_confirmed']}")
    print(f"     • Annulées: {stats['orders_cancelled']}")
    print(f"   - Notifications non lues: {stats['unread_notifications']}")
    
    # Top vendeurs
    from django.db.models import Count
    top_sellers = User.objects.filter(role='seller').annotate(
        articles_count=Count('articles')
    ).order_by('-articles_count')[:5]
    
    print(f"\n🏆 Top 5 vendeurs:")
    for i, seller in enumerate(top_sellers, 1):
        print(f"   {i}. {seller.get_full_name() or seller.username}: {seller.articles_count} article(s)")
    
    # Articles récents
    recent_articles = Article.objects.select_related('seller').order_by('-created_at')[:5]
    print(f"\n📦 Articles récents:")
    for article in recent_articles:
        print(f"   - {article.title} ({article.price}€) par {article.seller.username}")
    
    # Commandes récentes
    recent_orders = Order.objects.select_related('article', 'seller').order_by('-created_at')[:5]
    print(f"\n🛒 Commandes récentes:")
    for order in recent_orders:
        status_emoji = {'pending': '⏳', 'confirmed': '✅', 'cancelled': '❌'}
        print(f"   - #{order.id}: {order.client_name} → {order.article.title} {status_emoji.get(order.status, '❓')}")
    
    # URLs de test
    print(f"\n🌐 URLs du dashboard admin:")
    print(f"   - Dashboard principal: http://127.0.0.1:8000/admin-dashboard/")
    print(f"   - Gestion utilisateurs: http://127.0.0.1:8000/admin-dashboard/users/")
    print(f"   - Gestion articles: http://127.0.0.1:8000/admin-dashboard/articles/")
    print(f"   - Gestion commandes: http://127.0.0.1:8000/admin-dashboard/orders/")
    print(f"   - Notifications: http://127.0.0.1:8000/admin-dashboard/notifications/")
    print(f"   - Statistiques: http://127.0.0.1:8000/admin-dashboard/stats/")
    
    print(f"\n🔑 Connexion admin:")
    print(f"   - Username: {admin.username}")
    print(f"   - Email: {admin.email}")
    print(f"   - URL connexion: http://127.0.0.1:8000/login/")
    
    # Test des permissions
    print(f"\n🔒 Test des permissions:")
    
    # Vérifier les rôles
    roles_count = {
        'admin': User.objects.filter(role='admin').count(),
        'seller': User.objects.filter(role='seller').count(),
        'client': User.objects.filter(role='client').count(),
    }
    
    for role, count in roles_count.items():
        print(f"   - {role.capitalize()}: {count} utilisateur(s)")
    
    # Vérifier les utilisateurs actifs/inactifs
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()
    
    print(f"   - Utilisateurs actifs: {active_users}")
    print(f"   - Utilisateurs inactifs: {inactive_users}")
    
    print(f"\n🎉 Test du dashboard admin terminé !")
    print(f"\n💡 Pour tester le dashboard admin:")
    print(f"   1. Allez sur http://127.0.0.1:8000/login/")
    print(f"   2. Connectez-vous avec: {admin.username} / admin123")
    print(f"   3. Allez sur http://127.0.0.1:8000/admin-dashboard/")

if __name__ == '__main__':
    test_admin_dashboard()
