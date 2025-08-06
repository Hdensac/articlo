#!/usr/bin/env python
"""
Script pour créer plus d'articles pour tester la pagination
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
import random

def create_more_articles():
    print("📦 Création d'articles supplémentaires pour tester la pagination...")
    
    # Récupérer les vendeurs existants
    sellers = list(User.objects.filter(role='seller'))
    if not sellers:
        print("❌ Aucun vendeur trouvé. Exécutez d'abord create_test_data.py")
        return
    
    # Articles supplémentaires
    additional_articles = [
        {
            'title': 'Tablette iPad Air',
            'description': 'iPad Air 64GB WiFi, écran 10.9 pouces, puce A14 Bionic. Excellent état.',
            'price': Decimal('449.99'),
        },
        {
            'title': 'Écouteurs AirPods Pro',
            'description': 'AirPods Pro avec réduction de bruit active, boîtier de charge sans fil.',
            'price': Decimal('199.99'),
        },
        {
            'title': 'Clavier mécanique Gaming',
            'description': 'Clavier mécanique RGB, switches Cherry MX Blue, parfait pour le gaming.',
            'price': Decimal('89.99'),
        },
        {
            'title': 'Souris gaming Logitech',
            'description': 'Souris gaming haute précision, 12000 DPI, éclairage RGB personnalisable.',
            'price': Decimal('59.99'),
        },
        {
            'title': 'Webcam HD 1080p',
            'description': 'Webcam Full HD avec micro intégré, parfaite pour le télétravail.',
            'price': Decimal('39.99'),
        },
        {
            'title': 'Disque dur externe 2TB',
            'description': 'Disque dur externe USB 3.0, 2TB de stockage, compact et rapide.',
            'price': Decimal('79.99'),
        },
        {
            'title': 'Enceinte Bluetooth JBL',
            'description': 'Enceinte portable étanche, son puissant, autonomie 20h.',
            'price': Decimal('69.99'),
        },
        {
            'title': 'Chargeur sans fil',
            'description': 'Chargeur sans fil rapide 15W, compatible iPhone et Android.',
            'price': Decimal('24.99'),
        },
        {
            'title': 'Coque iPhone transparente',
            'description': 'Coque de protection transparente, anti-choc, compatible MagSafe.',
            'price': Decimal('19.99'),
        },
        {
            'title': 'Support téléphone bureau',
            'description': 'Support ajustable pour téléphone et tablette, aluminium premium.',
            'price': Decimal('29.99'),
        },
        {
            'title': 'Câble USB-C vers Lightning',
            'description': 'Câble de charge rapide 2m, certifié MFi, tressage nylon.',
            'price': Decimal('15.99'),
        },
        {
            'title': 'Powerbank 20000mAh',
            'description': 'Batterie externe haute capacité, charge rapide, 3 ports USB.',
            'price': Decimal('34.99'),
        },
        {
            'title': 'Lampe LED bureau',
            'description': 'Lampe de bureau LED avec variateur, port USB, design moderne.',
            'price': Decimal('49.99'),
        },
        {
            'title': 'Tapis de souris XXL',
            'description': 'Tapis de souris gaming extra large, surface lisse, base antidérapante.',
            'price': Decimal('19.99'),
        },
        {
            'title': 'Hub USB-C 7 en 1',
            'description': 'Hub multiport avec HDMI 4K, USB 3.0, lecteur SD, charge PD.',
            'price': Decimal('44.99'),
        },
    ]
    
    created_count = 0
    for article_data in additional_articles:
        # Assigner un vendeur aléatoire
        article_data['seller'] = random.choice(sellers)
        
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults=article_data
        )
        if created:
            print(f"✅ Article créé: {article.title} ({article.price}€)")
            created_count += 1
        else:
            print(f"ℹ️  Article existe déjà: {article.title}")
    
    # Statistiques finales
    total_articles = Article.objects.count()
    print(f"\n🎉 {created_count} nouveaux articles créés !")
    print(f"📊 Total articles: {total_articles}")
    
    # Vérifier la pagination
    if total_articles > 12:
        pages = (total_articles + 11) // 12  # Arrondir vers le haut
        print(f"📄 Pagination: {pages} page(s) (12 articles par page)")
        print(f"🌐 Test pagination: http://127.0.0.1:8000/?page=2")
    
    print(f"\n🔍 URLs de test avec plus d'articles:")
    print(f"   - Recherche 'gaming': http://127.0.0.1:8000/?search=gaming")
    print(f"   - Articles tech < 50€: http://127.0.0.1:8000/?search=USB&price_range=0-50")
    print(f"   - Tri par prix croissant: http://127.0.0.1:8000/?sort_by=price")

if __name__ == '__main__':
    create_more_articles()
