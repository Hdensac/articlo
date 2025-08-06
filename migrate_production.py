#!/usr/bin/env python
"""
Script de migration pour la production Render
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from users.models import User

def migrate_production():
    print("🚀 Migration vers la production...")
    
    # Appliquer les migrations
    print("📊 Application des migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collecter les fichiers statiques
    print("📁 Collecte des fichiers statiques...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Créer un superutilisateur si nécessaire
    User = get_user_model()
    
    admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@articlo.com')
    admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    if not User.objects.filter(username=admin_username).exists():
        print(f"👑 Création du superutilisateur {admin_username}...")
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            role='admin'
        )
        print(f"✅ Superutilisateur créé avec succès!")
    else:
        print(f"✅ Superutilisateur {admin_username} existe déjà")
    
    print("🎉 Migration terminée avec succès!")

if __name__ == '__main__':
    migrate_production()
