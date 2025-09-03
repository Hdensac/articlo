# 🚀 Déploiement Rapide - Solution Images Render

## Problème résolu ✅

Les vendeurs ne peuvent pas voir les images de leurs articles sur Render car les fichiers ne sont pas persistés.

## Solution immédiate (5 minutes)

### Option 1 : AWS S3 (Recommandé)

1. **Créer un compte AWS S3 gratuit**
   - Allez sur [aws.amazon.com](https://aws.amazon.com)
   - Créez un bucket S3 (ex: `articlo-images-2024`)

2. **Configurer les variables sur Render**
   - Dans votre dashboard Render
   - Allez dans "Environment Variables"
   - Ajoutez :
     ```
     AWS_ACCESS_KEY_ID=votre_clé_access
     AWS_SECRET_ACCESS_KEY=votre_clé_secrète
     AWS_STORAGE_BUCKET_NAME=votre_bucket
     AWS_S3_REGION_NAME=us-east-1
     ```

3. **Redéployer**
   - Cliquez sur "Manual Deploy" sur Render
   - Attendez la fin du déploiement

### Option 2 : Solution temporaire (Sans AWS)

Si vous ne voulez pas configurer AWS maintenant :

1. **Redéployer l'application**
   - Le code est déjà configuré pour une solution temporaire
   - Les images seront copiées dans le dossier statique

⚠️ **Attention** : Cette solution perd les images à chaque redémarrage

## Vérification

Après déploiement :
1. Allez sur votre site
2. Connectez-vous en tant que vendeur
3. Créez un article avec une image
4. Vérifiez que l'image s'affiche

## Support

- **Avec AWS S3** : Images persistantes ✅
- **Sans AWS** : Images temporaires ⚠️

## Prochaines étapes

Pour une solution permanente, configurez AWS S3 ou un service similaire.
