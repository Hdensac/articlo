#!/usr/bin/env bash
# Script de build simplifié pour Render

set -o errexit

echo "🚀 Build Articlo - Version simplifiée"

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate

echo "✅ Build terminé"
