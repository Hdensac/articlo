"""
Configuration Django pour Render (Production)
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Hosts autorisés
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.onrender.com,127.0.0.1,localhost').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'users',
    'articles',
    'dashboard',
    'orders',
    'notifications',
]

# Activer Cloudinary si la variable est configurée
if os.environ.get('CLOUDINARY_URL'):
    INSTALLED_APPS += [
        'cloudinary',
        'cloudinary_storage',
    ]
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    # Optionnel: configuration explicite (la variable CLOUDINARY_URL suffit normalement)
    # CLOUDINARY_STORAGE = {
    #     'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    #     'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    #     'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    # }
    try:
        print("✅ Cloudinary détecté via CLOUDINARY_URL — backend activé: cloudinary_storage.storage.MediaCloudinaryStorage")
    except Exception:
        pass

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.MediaFilesMiddleware',  # Middleware pour les fichiers média
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuration pour servir les fichiers média en production
if not DEBUG:
    # Utiliser WhiteNoise pour les fichiers statiques
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Configuration pour les fichiers média
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    
    # SOLUTION IMMÉDIATE : Forcer l'utilisation d'AWS S3 ou d'un service cloud
    # Si AWS S3 n'est pas configuré, utiliser Cloudinary (gratuit)
    
    # Vérifier d'abord AWS S3
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
        # Utiliser AWS S3 pour les fichiers média
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
        print("✅ Configuration AWS S3 activée pour les fichiers média")
    else:
        # Solution de secours : Utiliser Cloudinary (gratuit)
        CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
        if CLOUDINARY_URL:
            DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
            print("✅ Configuration Cloudinary activée pour les fichiers média")
        else:
            # DERNIÈRE SOLUTION : Copier les images dans staticfiles
            # ATTENTION : Cette solution perd les images à chaque redémarrage
            MEDIA_ROOT = STATIC_ROOT / 'media'
            MEDIA_URL = '/static/media/'
            print("⚠️ ATTENTION : Utilisation du stockage local temporaire - les images seront perdues à chaque redémarrage")
            print("💡 Pour une solution permanente, configurez AWS S3 ou Cloudinary")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Authentication settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Configuration de sécurité pour la production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
