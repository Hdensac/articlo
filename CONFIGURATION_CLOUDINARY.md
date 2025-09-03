# 🚀 Configuration Cloudinary - Solution Gratuite pour les Images

## Pourquoi Cloudinary ?

- **Gratuit** jusqu'à 25GB de stockage
- **Configuration simple** en 2 minutes
- **Pas besoin de carte bancaire**
- **Images optimisées automatiquement**

## Configuration en 2 minutes

### 1. Créer un compte Cloudinary

1. Allez sur [cloudinary.com](https://cloudinary.com)
2. Cliquez sur "Sign Up For Free"
3. Créez votre compte (email + mot de passe)
4. Notez vos informations de connexion

### 2. Récupérer vos clés

Après connexion, allez dans votre **Dashboard** et copiez :
- **Cloud Name**
- **API Key** 
- **API Secret**

### 3. Configurer sur Render

Dans votre dashboard Render, ajoutez cette variable d'environnement :

```
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

**Exemple :**
```
CLOUDINARY_URL=cloudinary://123456789:abcdefghijklmnop@moncompte
```

### 4. Redéployer

1. Cliquez sur "Manual Deploy" sur Render
2. Attendez la fin du déploiement
3. Testez l'upload d'images

## Vérification

Après déploiement :
- ✅ Les images s'affichent
- ✅ Les nouveaux uploads fonctionnent
- ✅ Les images persistent entre les redémarrages
- ✅ Pas de perte de données

## Avantages vs AWS S3

| Aspect | Cloudinary | AWS S3 |
|--------|------------|---------|
| **Prix** | Gratuit 25GB | Payant |
| **Configuration** | 2 minutes | 15+ minutes |
| **Carte bancaire** | Non | Oui |
| **Support** | Excellent | Basique |

## Support

- **Documentation** : [cloudinary.com/documentation](https://cloudinary.com/documentation)
- **Limite gratuite** : 25GB de stockage
- **Types d'images** : JPG, PNG, GIF, WebP, etc.

## Alternative

Si vous préférez AWS S3, suivez le guide `DEPLOIEMENT_RAPIDE.md`.

