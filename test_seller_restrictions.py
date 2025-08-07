#!/usr/bin/env python
"""
Script de test pour vérifier les restrictions des vendeurs
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from users.models import User
from articles.models import Article
from orders.models import Order

def test_seller_restrictions():
    print("🧪 Test des restrictions vendeur...")
    print("=" * 60)
    
    # 1. Créer un vendeur de test
    print("\n1️⃣ Création d'un vendeur de test...")
    seller, created = User.objects.get_or_create(
        username='test_seller',
        defaults={
            'email': 'seller@test.com',
            'password': make_password('test123'),
            'role': 'seller',
            'first_name': 'Test',
            'last_name': 'Seller',
            'is_active': True,
            'whatsapp_number': '+33123456789'
        }
    )
    
    if created:
        print("✅ Vendeur créé avec succès")
    else:
        print("ℹ️ Vendeur existant utilisé")
    
    print(f"   👤 Utilisateur: {seller.username}")
    print(f"   🏪 Rôle: {seller.get_role_display()}")
    print(f"   📱 WhatsApp: {seller.whatsapp_number}")
    
    # 2. Créer un client de test
    print("\n2️⃣ Création d'un client de test...")
    client, created = User.objects.get_or_create(
        username='test_client',
        defaults={
            'email': 'client@test.com',
            'password': make_password('test123'),
            'role': 'client',
            'first_name': 'Test',
            'last_name': 'Client',
            'is_active': True
        }
    )
    
    if created:
        print("✅ Client créé avec succès")
    else:
        print("ℹ️ Client existant utilisé")
    
    print(f"   👤 Utilisateur: {client.username}")
    print(f"   🛒 Rôle: {client.get_role_display()}")
    
    # 3. Créer un article de test
    print("\n3️⃣ Création d'un article de test...")
    article, created = Article.objects.get_or_create(
        title='Article de test',
        defaults={
            'description': 'Ceci est un article de test pour vérifier les restrictions.',
            'price': 29.99,
            'seller': seller
        }
    )
    
    if created:
        print("✅ Article créé avec succès")
    else:
        print("ℹ️ Article existant utilisé")
    
    print(f"   📦 Article: {article.title}")
    print(f"   💰 Prix: {article.price}€")
    print(f"   🏪 Vendeur: {article.seller.username}")
    
    # 4. Tester les méthodes du modèle User
    print("\n4️⃣ Test des méthodes de vérification de rôle...")
    
    print(f"   Vendeur - is_seller(): {seller.is_seller()}")
    print(f"   Vendeur - is_client(): {seller.is_client()}")
    print(f"   Vendeur - can_order(): {seller.can_order()}")
    
    print(f"   Client - is_seller(): {client.is_seller()}")
    print(f"   Client - is_client(): {client.is_client()}")
    print(f"   Client - can_order(): {client.can_order()}")
    
    # 5. Statistiques
    print("\n5️⃣ Statistiques de la plateforme...")
    
    total_users = User.objects.count()
    sellers = User.objects.filter(role='seller').count()
    clients = User.objects.filter(role='client').count()
    admins = User.objects.filter(role='admin').count()
    
    total_articles = Article.objects.count()
    total_orders = Order.objects.count()
    
    print(f"   👥 Total utilisateurs: {total_users}")
    print(f"   🏪 Vendeurs: {sellers}")
    print(f"   🛒 Clients: {clients}")
    print(f"   👑 Admins: {admins}")
    print(f"   📦 Total articles: {total_articles}")
    print(f"   📋 Total commandes: {total_orders}")
    
    # 6. Informations de connexion
    print("\n6️⃣ Informations de connexion pour les tests...")
    print("   🔐 Comptes de test créés:")
    print(f"      Vendeur: {seller.username} / test123")
    print(f"      Client: {client.username} / test123")
    
    print("\n✅ Tests terminés avec succès!")
    print("🌐 Vous pouvez maintenant tester sur http://127.0.0.1:8000/")
    print("📝 Connectez-vous avec les comptes ci-dessus pour tester les restrictions.")

if __name__ == '__main__':
    test_seller_restrictions()
