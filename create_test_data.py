#!/usr/bin/env python
"""
Script pour créer des données de test pour l'application Articlo
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from articles.models import Article
from decimal import Decimal

def create_test_data():
    print("🚀 Création des données de test...")
    
    # Créer des utilisateurs vendeurs
    sellers_data = [
        {
            'username': 'marie_boutique',
            'email': 'marie@example.com',
            'first_name': 'Marie',
            'last_name': 'Dupont',
            'role': 'seller',
            'whatsapp_number': '+33123456789'
        },
        {
            'username': 'tech_store',
            'email': 'tech@example.com',
            'first_name': 'Jean',
            'last_name': 'Martin',
            'role': 'seller',
            'whatsapp_number': '+33987654321'
        },
        {
            'username': 'fashion_world',
            'email': 'fashion@example.com',
            'first_name': 'Sophie',
            'last_name': 'Bernard',
            'role': 'seller',
            'whatsapp_number': '+33555666777'
        }
    ]
    
    sellers = []
    for seller_data in sellers_data:
        seller, created = User.objects.get_or_create(
            username=seller_data['username'],
            defaults=seller_data
        )
        if created:
            seller.set_password('password123')
            seller.save()
            print(f"✅ Vendeur créé: {seller.username}")
        else:
            print(f"ℹ️  Vendeur existe déjà: {seller.username}")
        sellers.append(seller)
    
    # Créer des articles
    articles_data = [
        {
            'title': 'iPhone 14 Pro Max',
            'description': 'iPhone 14 Pro Max 256GB, état neuf, avec boîte et accessoires. Écran Super Retina XDR de 6,7 pouces.',
            'price': Decimal('899.99'),
            'seller': sellers[1]  # tech_store
        },
        {
            'title': 'Robe d\'été fleurie',
            'description': 'Magnifique robe d\'été en coton bio, motifs floraux, taille M. Parfaite pour les beaux jours.',
            'price': Decimal('45.00'),
            'seller': sellers[2]  # fashion_world
        },
        {
            'title': 'MacBook Air M2',
            'description': 'MacBook Air avec puce M2, 8GB RAM, 256GB SSD. Excellent état, utilisé 6 mois seulement.',
            'price': Decimal('1199.00'),
            'seller': sellers[1]  # tech_store
        },
        {
            'title': 'Sac à main cuir',
            'description': 'Sac à main en cuir véritable, couleur cognac, plusieurs compartiments. Très bon état.',
            'price': Decimal('89.99'),
            'seller': sellers[0]  # marie_boutique
        },
        {
            'title': 'Casque Bluetooth Sony',
            'description': 'Casque Sony WH-1000XM4, réduction de bruit active, autonomie 30h. Comme neuf.',
            'price': Decimal('249.99'),
            'seller': sellers[1]  # tech_store
        },
        {
            'title': 'Chaussures de sport Nike',
            'description': 'Nike Air Max 90, taille 42, couleur blanc/noir. Portées quelques fois seulement.',
            'price': Decimal('79.99'),
            'seller': sellers[2]  # fashion_world
        },
        {
            'title': 'Montre connectée Apple Watch',
            'description': 'Apple Watch Series 8, 45mm, GPS + Cellular. Bracelet sport inclus.',
            'price': Decimal('399.00'),
            'seller': sellers[1]  # tech_store
        },
        {
            'title': 'Veste en jean vintage',
            'description': 'Veste en jean vintage années 90, taille L, délavage parfait. Pièce unique.',
            'price': Decimal('35.00'),
            'seller': sellers[2]  # fashion_world
        },
        {
            'title': 'Parfum Chanel N°5',
            'description': 'Parfum Chanel N°5 100ml, neuf sous blister. Cadeau non utilisé.',
            'price': Decimal('129.99'),
            'seller': sellers[0]  # marie_boutique
        },
        {
            'title': 'Console PlayStation 5',
            'description': 'PlayStation 5 avec lecteur disque, 2 manettes, 3 jeux inclus. État impeccable.',
            'price': Decimal('549.99'),
            'seller': sellers[1]  # tech_store
        }
    ]
    
    for article_data in articles_data:
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults=article_data
        )
        if created:
            print(f"✅ Article créé: {article.title}")
        else:
            print(f"ℹ️  Article existe déjà: {article.title}")
    
    print(f"\n🎉 Données de test créées avec succès !")
    print(f"📊 Statistiques:")
    print(f"   - Vendeurs: {User.objects.filter(role='seller').count()}")
    print(f"   - Articles: {Article.objects.count()}")
    print(f"\n🌐 Visitez http://127.0.0.1:8000 pour voir le résultat !")

if __name__ == '__main__':
    create_test_data()
