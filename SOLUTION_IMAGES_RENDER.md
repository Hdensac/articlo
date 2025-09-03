# Solution pour le problème des images sur Render

## Problème identifié

Sur Render, les vendeurs ne peuvent pas voir les images de leurs articles car :

1. **Render ne persiste pas les fichiers uploadés** entre les redémarrages
2. **Les fichiers média ne sont pas servis correctement** en production
3. **WhiteNoise** ne gère que les fichiers statiques, pas les fichiers média

## Solutions disponibles

### Solution 1 : Service de stockage cloud (Recommandé)

Utilisez AWS S3 ou un service similaire pour stocker les images de manière permanente.

#### Configuration AWS S3

1. **Installer la dépendance** :
```bash
pip install django-storages
```

2. **Ajouter aux requirements.txt** :
```
django-storages>=1.14
boto3>=1.26
```

3. **Configurer les variables d'environnement sur Render** :
```
AWS_ACCESS_KEY_ID=votre_clé_access
AWS_SECRET_ACCESS_KEY=votre_clé_secrète
AWS_STORAGE_BUCKET_NAME=votre_bucket
AWS_S3_REGION_NAME=us-east-1
```

4. **Modifier config/settings_render.py** :
```python
# Décommentez ces lignes
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

### Solution 2 : Service de stockage gratuit

Utilisez des services gratuits comme :
- **Cloudinary** (gratuit jusqu'à 25GB)
- **ImgBB** (gratuit)
- **Firebase Storage** (gratuit jusqu'à 5GB)

### Solution 3 : Stockage local temporaire (Non recommandé)

Cette solution copie les images dans le dossier statique mais les perd à chaque redémarrage.

## Instructions de déploiement

1. **Choisir une solution** (AWS S3 recommandé)
2. **Configurer les variables d'environnement** sur Render
3. **Redéployer l'application**
4. **Tester l'upload d'images**

## Vérification

Après déploiement, vérifiez que :
- Les images s'affichent correctement
- Les nouveaux uploads fonctionnent
- Les images persistent entre les redémarrages

## Support

Pour toute question, consultez la documentation de Django et du service de stockage choisi.
