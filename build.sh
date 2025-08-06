#!/usr/bin/env bash
# Script de build pour Render - Articlo

set -o errexit  # Exit on error

echo "🚀 Début du build Articlo..."

# Mettre à jour pip
echo "🔧 Mise à jour de pip..."
python -m pip install --upgrade pip

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations de base de données
echo "🗄️ Application des migrations..."
python manage.py migrate

# Créer un superutilisateur si les variables d'environnement sont définies
if [[ $CREATE_SUPERUSER == "True" ]]; then
    echo "👑 Création du superutilisateur..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import os

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@articlo.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

try:
    user = User.objects.get(username=username)
    print(f"✅ Superutilisateur '{username}' existe déjà")
except ObjectDoesNotExist:
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin'
    )
    print(f"✅ Superutilisateur '{username}' créé avec succès")
EOF
fi

# Créer des données de test si demandé
if [[ $CREATE_TEST_DATA == "True" ]]; then
    echo "🧪 Création des données de test..."
    python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from articles.models import Article
from django.contrib.auth.hashers import make_password

# Créer quelques vendeurs de test
sellers_data = [
    {'username': 'tech_store', 'email': 'tech@articlo.com', 'first_name': 'Tech', 'last_name': 'Store'},
    {'username': 'fashion_world', 'email': 'fashion@articlo.com', 'first_name': 'Fashion', 'last_name': 'World'},
    {'username': 'marie_boutique', 'email': 'marie@articlo.com', 'first_name': 'Marie', 'last_name': 'Boutique'},
]

for seller_data in sellers_data:
    seller, created = User.objects.get_or_create(
        username=seller_data['username'],
        defaults={
            'email': seller_data['email'],
            'password': make_password('vendeur123'),
            'role': 'seller',
            'first_name': seller_data['first_name'],
            'last_name': seller_data['last_name'],
            'is_active': True,
            'whatsapp_number': '+33123456789'
        }
    )
    if created:
        print(f'✅ Vendeur {seller.username} créé')

# Créer quelques articles de démonstration
articles_data = [
    {
        'title': 'iPhone 14 Pro Max',
        'description': 'Smartphone Apple dernière génération, état neuf, avec tous les accessoires.',
        'price': 1200.00,
        'seller_username': 'tech_store'
    },
    {
        'title': 'MacBook Air M2',
        'description': 'Ordinateur portable Apple avec puce M2, 8GB RAM, 256GB SSD.',
        'price': 1400.00,
        'seller_username': 'tech_store'
    },
    {
        'title': 'Robe d\'été élégante',
        'description': 'Belle robe d\'été, taille M, parfaite pour les occasions spéciales.',
        'price': 89.99,
        'seller_username': 'fashion_world'
    },
    {
        'title': 'Sac à main cuir',
        'description': 'Sac à main en cuir véritable, couleur marron, très bon état.',
        'price': 150.00,
        'seller_username': 'marie_boutique'
    },
]

for article_data in articles_data:
    try:
        seller = User.objects.get(username=article_data['seller_username'])
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            seller=seller,
            defaults={
                'description': article_data['description'],
                'price': article_data['price'],
            }
        )
        if created:
            print(f'✅ Article {article.title} créé')
    except User.DoesNotExist:
        print(f'❌ Vendeur {article_data[\"seller_username\"]} non trouvé')

print('🎉 Données de test créées avec succès!')
"
fi

echo "✅ Build terminé avec succès!"
