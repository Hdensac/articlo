#!/usr/bin/env python
"""
Script pour tester le système de recherche et filtres
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from articles.models import Article
from articles.forms import ArticleSearchForm
from users.models import User
from django.db.models import Q

def test_search_system():
    print("🔍 Test du système de recherche et filtres...")
    
    # Statistiques générales
    total_articles = Article.objects.count()
    total_sellers = User.objects.filter(role='seller').count()
    
    print(f"📊 Données disponibles:")
    print(f"   - Articles totaux: {total_articles}")
    print(f"   - Vendeurs actifs: {total_sellers}")
    
    # Test 1: Recherche textuelle
    print(f"\n🔍 Test 1: Recherche textuelle")
    search_terms = ['iPhone', 'MacBook', 'robe', 'casque', 'montre']
    
    for term in search_terms:
        results = Article.objects.filter(
            Q(title__icontains=term) | Q(description__icontains=term)
        )
        print(f"   - '{term}': {results.count()} résultat(s)")
        if results.exists():
            for article in results[:2]:  # Afficher les 2 premiers
                print(f"     → {article.title} ({article.price}€)")
    
    # Test 2: Filtres par prix
    print(f"\n💰 Test 2: Filtres par prix")
    price_ranges = [
        ('0-50', 'Moins de 50€'),
        ('50-100', '50€ - 100€'),
        ('100-250', '100€ - 250€'),
        ('250-500', '250€ - 500€'),
        ('500-1000', '500€ - 1000€'),
        ('1000+', 'Plus de 1000€'),
    ]
    
    for range_key, range_label in price_ranges:
        if range_key == '0-50':
            results = Article.objects.filter(price__lt=50)
        elif range_key == '50-100':
            results = Article.objects.filter(price__gte=50, price__lt=100)
        elif range_key == '100-250':
            results = Article.objects.filter(price__gte=100, price__lt=250)
        elif range_key == '250-500':
            results = Article.objects.filter(price__gte=250, price__lt=500)
        elif range_key == '500-1000':
            results = Article.objects.filter(price__gte=500, price__lt=1000)
        elif range_key == '1000+':
            results = Article.objects.filter(price__gte=1000)
        
        print(f"   - {range_label}: {results.count()} article(s)")
        if results.exists():
            for article in results[:2]:
                print(f"     → {article.title} ({article.price}€)")
    
    # Test 3: Filtres par vendeur
    print(f"\n👤 Test 3: Filtres par vendeur")
    sellers = User.objects.filter(role='seller')[:5]
    
    for seller in sellers:
        articles = Article.objects.filter(seller=seller)
        print(f"   - {seller.username}: {articles.count()} article(s)")
        if articles.exists():
            for article in articles[:2]:
                print(f"     → {article.title} ({article.price}€)")
    
    # Test 4: Tri
    print(f"\n📊 Test 4: Options de tri")
    sort_options = [
        ('-created_at', 'Plus récents'),
        ('created_at', 'Plus anciens'),
        ('price', 'Prix croissant'),
        ('-price', 'Prix décroissant'),
        ('title', 'Nom A-Z'),
        ('-title', 'Nom Z-A'),
    ]
    
    for sort_key, sort_label in sort_options:
        results = Article.objects.all().order_by(sort_key)[:3]
        print(f"   - {sort_label}:")
        for article in results:
            print(f"     → {article.title} ({article.price}€) - {article.created_at.strftime('%d/%m/%Y')}")
    
    # Test 5: Formulaire de recherche
    print(f"\n📝 Test 5: Validation du formulaire")
    
    # Test avec données valides
    form_data = {
        'search': 'iPhone',
        'min_price': '100',
        'max_price': '1000',
        'sort_by': '-price'
    }
    
    form = ArticleSearchForm(data=form_data)
    if form.is_valid():
        print("   ✅ Formulaire valide avec données correctes")
    else:
        print("   ❌ Erreur de validation:", form.errors)
    
    # Test avec prix invalide
    form_data_invalid = {
        'min_price': '1000',
        'max_price': '100',  # Prix max < prix min
    }
    
    form_invalid = ArticleSearchForm(data=form_data_invalid)
    if not form_invalid.is_valid():
        print("   ✅ Validation correcte: prix min > prix max détecté")
    else:
        print("   ❌ Erreur: validation devrait échouer")
    
    # Test 6: URLs de test
    print(f"\n🌐 URLs de test:")
    print(f"   - Page d'accueil: http://127.0.0.1:8000/")
    print(f"   - Recherche iPhone: http://127.0.0.1:8000/?search=iPhone")
    print(f"   - Prix 100-250€: http://127.0.0.1:8000/?price_range=100-250")
    print(f"   - Tri par prix: http://127.0.0.1:8000/?sort_by=price")
    print(f"   - Recherche combinée: http://127.0.0.1:8000/?search=iPhone&sort_by=-price&price_range=500-1000")
    
    print(f"\n🎉 Test du système de recherche terminé !")

if __name__ == '__main__':
    test_search_system()
