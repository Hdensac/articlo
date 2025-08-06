#!/usr/bin/env python
"""
Script pour vérifier les utilisateurs et leurs mots de passe
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from django.contrib.auth.hashers import make_password

def check_users():
    print("🔍 Vérification des utilisateurs...")
    
    users = User.objects.all().order_by('role', 'username')
    
    print(f"\n📊 {users.count()} utilisateurs trouvés :")
    print("-" * 80)
    
    for user in users:
        role_emoji = {
            'admin': '👑',
            'seller': '🏪',
            'client': '👤'
        }
        
        status = "✅ Actif" if user.is_active else "❌ Inactif"
        
        print(f"{role_emoji.get(user.role, '❓')} {user.role.upper():<8} | {user.username:<15} | {user.email:<25} | {status}")
        
        # Informations supplémentaires pour les vendeurs
        if user.role == 'seller':
            articles_count = user.articles.count() if hasattr(user, 'articles') else 0
            print(f"    📦 Articles: {articles_count}")
            if user.whatsapp_number:
                print(f"    📱 WhatsApp: {user.whatsapp_number}")
    
    print("-" * 80)
    
    # Créer un vendeur de test avec un mot de passe simple
    print("\n🔧 Création d'un vendeur de test...")
    
    test_seller, created = User.objects.get_or_create(
        username='vendeur_test',
        defaults={
            'email': 'vendeur@test.com',
            'password': make_password('123456'),  # Mot de passe simple
            'role': 'seller',
            'first_name': 'Vendeur',
            'last_name': 'Test',
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Vendeur de test créé !")
    else:
        # Mettre à jour le mot de passe au cas où
        test_seller.set_password('123456')
        test_seller.save()
        print(f"✅ Vendeur de test mis à jour !")
    
    print(f"\n🔑 Comptes de test disponibles :")
    print(f"   👑 ADMIN:")
    print(f"      Username: admin")
    print(f"      Password: admin123")
    print(f"      URL: http://127.0.0.1:8000/login/")
    
    print(f"\n   🏪 VENDEUR:")
    print(f"      Username: vendeur_test")
    print(f"      Password: 123456")
    print(f"      URL: http://127.0.0.1:8000/login/")
    
    # Vérifier les vendeurs existants
    sellers = User.objects.filter(role='seller', is_active=True)
    if sellers.exists():
        print(f"\n   🏪 AUTRES VENDEURS ACTIFS:")
        for seller in sellers:
            print(f"      Username: {seller.username}")
            print(f"      Email: {seller.email}")
            # Réinitialiser le mot de passe pour faciliter les tests
            seller.set_password('vendeur123')
            seller.save()
            print(f"      Password: vendeur123 (réinitialisé)")
            print()
    
    print(f"\n💡 Conseils de connexion :")
    print(f"   - Vérifiez que le username est exact (sensible à la casse)")
    print(f"   - Vérifiez que le mot de passe est exact")
    print(f"   - Essayez d'abord avec 'vendeur_test' / '123456'")
    print(f"   - Si ça ne marche pas, essayez les autres vendeurs avec 'vendeur123'")

if __name__ == '__main__':
    check_users()
