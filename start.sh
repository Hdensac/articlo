#!/bin/bash
# Script de démarrage pour Render

echo "🚀 Démarrage d'Articlo..."

# Démarrer Gunicorn avec la configuration Django
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
