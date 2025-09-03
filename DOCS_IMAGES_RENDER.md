# Problème d’images en production (Render) — Diagnostic et Résolution

## Contexte
- En local: les images d’articles s’affichent correctement.
- En production (Render): les images renvoient 404, par exemple `/media/articles/xxx.jpeg`.

## Symptômes observés
- Logs Render: `Not Found: /media/...`
- Au démarrage: `⚠️ Configuration AWS S3 non trouvée, utilisation du stockage local temporaire`
- Les pages d’articles s’affichent, mais les `<img src="/media/...">` ne chargent pas.

## Causes racines
1. Le stockage par défaut pointait vers le **système de fichiers local** (`MEDIA_ROOT`) qui n’est **pas persistant** sur Render.
2. Les URLs des images restent en `/media/...` en production → Django ne peut pas servir ces fichiers (et WhiteNoise ne gère pas les médias dynamiques).
3. Initialement, **`DJANGO_SETTINGS_MODULE` n’était pas défini** sur `config.settings_render`, donc la configuration prod n’était pas entièrement appliquée.
4. La variable **`CLOUDINARY_URL`** n’était pas prise en compte au runtime, donc le backend cloud n’était pas activé → fallback en stockage local temporaire.

## Solution choisie
Passage au **stockage cloud avec Cloudinary** (gratuit, simple, persistant) et activation conditionnelle côté Django.

## Changements effectués (code)
- `config/settings_render.py`:
  - Ajout conditionnel de `cloudinary` et `cloudinary_storage` dans `INSTALLED_APPS` si `CLOUDINARY_URL` est présent.
  - Forçage du backend médias: `DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'` quand `CLOUDINARY_URL` est défini.
  - Logs explicites au démarrage pour indiquer le backend choisi.
- `requirements.txt`:
  - Ajout de `django-cloudinary-storage` (et conservation de `django-storages`/`boto3` si besoin d’AWS S3 ultérieurement).
- Guides ajoutés:
  - `CONFIGURATION_CLOUDINARY.md`, `DEPANNAGE_RAPIDE.md`, `DEPLOIEMENT_RAPIDE.md`, `SOLUTION_IMAGES_RENDER.md`.

## Changements effectués (Render)
- Variables d’environnement (service Web):
  - `DJANGO_SETTINGS_MODULE = config.settings_render`
  - `CLOUDINARY_URL = cloudinary://API_KEY:API_SECRET@CLOUD_NAME`
  - `ALLOWED_HOSTS` inclut le domaine `*.onrender.com`
  - `DEBUG = False`
- Redéploiement avec **Manual Deploy** en cochant **Clear build cache** (pour s’assurer de l’installation de `django-cloudinary-storage` et de la prise en compte des nouvelles variables).

## Procédure de vérification
1. Ouvrir les logs Render (All logs, sans filtre) après déploiement et vérifier un message proche de:
   - `Cloudinary détecté via CLOUDINARY_URL — backend activé: cloudinary_storage.storage.MediaCloudinaryStorage`
2. Éditer un article et **téléverser une NOUVELLE image**.
3. Dans le navigateur, copier l’adresse de l’image:
   - L’URL doit commencer par `https://res.cloudinary.com/...`
   - Si l’URL reste `/media/...`, refaire un upload (les anciennes images locales restent 404) et vérifier `CLOUDINARY_URL` + `DJANGO_SETTINGS_MODULE`.

## Points d’attention
- Les **anciennes images** qui pointent vers `/media/...` resteront **non disponibles** en prod. Il faut les **ré‑uploader** pour qu’elles soient envoyées sur Cloudinary.
- En cas de besoin d’AWS S3, prévoir: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME` et `DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'`. Ne pas activer S3 et Cloudinary en même temps.

## Résultat
- Les nouvelles images sont servies via Cloudinary (CDN), **persistantes** et **visibles en production**.
- La page liste/détail des articles affiche désormais correctement les vignettes et médias.

## Checklist rapide (runbook)
- [ ] `DJANGO_SETTINGS_MODULE = config.settings_render` sur le service Web
- [ ] `CLOUDINARY_URL` présent, sans guillemets, sans espaces
- [ ] `requirements.txt` contient `django-cloudinary-storage`
- [ ] Manual Deploy → Clear build cache
- [ ] Logs: message “Cloudinary détecté …”
- [ ] Upload d’une nouvelle image → URL `https://res.cloudinary.com/...`

## Annexes
- Erreur vue: `Not Found: /media/...`
- Log indicatif (fallback): `⚠️ Configuration AWS S3 non trouvée, utilisation du stockage local temporaire`
- Fichiers utiles: `config/settings_render.py`, `requirements.txt`, `render.yaml` (variables), templates affichant `{{ article.images.url }}`.
