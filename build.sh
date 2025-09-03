#!/bin/bash

# Script de build pour Render
echo "🚀 Démarrage du build..."

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Copier les fichiers média dans le dossier statique (solution temporaire pour Render)
echo "🖼️ Copie des fichiers média..."
if [ -d "media" ]; then
    mkdir -p staticfiles/media
    cp -r media/* staticfiles/media/ 2>/dev/null || echo "Aucun fichier média à copier"
fi

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate

echo "✅ Build terminé avec succès!"
