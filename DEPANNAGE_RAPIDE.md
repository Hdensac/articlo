# 🚨 Dépannage Rapide - Images qui ne s'affichent pas

## Problème actuel

❌ **En local** : Les images s'affichent ✅  
❌ **En ligne sur Render** : Les images ne s'affichent pas ❌

## Cause du problème

**Render ne persiste pas les fichiers uploadés** entre les redémarrages. C'est un comportement normal de Render.

## Solution immédiate (5 minutes)

### Option 1 : Cloudinary (GRATUIT - Recommandé)

1. **Créer un compte Cloudinary**
   - Allez sur [cloudinary.com](https://cloudinary.com)
   - Cliquez "Sign Up For Free"
   - Créez votre compte

2. **Récupérer vos clés**
   - Dans votre Dashboard Cloudinary
   - Copiez : **Cloud Name**, **API Key**, **API Secret**

3. **Configurer sur Render**
   - Dashboard Render → Environment Variables
   - Ajoutez :
     ```
     CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
     ```
   - **Exemple** : `cloudinary://123456789:abcdefghijklmnop@moncompte`

4. **Redéployer**
   - Cliquez "Manual Deploy" sur Render
   - Attendez la fin du déploiement

### Option 2 : AWS S3 (Payant)

Si vous préférez AWS S3, suivez le guide `DEPLOIEMENT_RAPIDE.md`.

## Vérification

Après déploiement :
1. Allez sur votre site en ligne
2. Connectez-vous en tant que vendeur
3. Créez un article avec une image
4. Vérifiez que l'image s'affiche

## Si le problème persiste

1. **Vérifiez les logs Render** pour voir les erreurs
2. **Testez la configuration** avec `python test_images.py`
3. **Vérifiez les variables d'environnement** sur Render

## Support

- **Cloudinary** : [cloudinary.com/documentation](https://cloudinary.com/documentation)
- **Limite gratuite** : 25GB de stockage
- **Pas de carte bancaire** requise

## Résultat attendu

✅ **Images visibles en ligne**  
✅ **Images persistantes** entre les redémarrages  
✅ **Uploads fonctionnels** pour les vendeurs

