import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# -------------------------
# Base
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'clave-local')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    "elportafoliodemarcos.onrender.com",
    "localhost",
    "127.0.0.1",
]

# -------------------------
# Apps
# -------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cloudinary',
    'cloudinary_storage',

    'portafolio',
]

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myportafolio.urls'
WSGI_APPLICATION = 'myportafolio.wsgi.application'

# -------------------------
# Templates
# -------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'portafolio' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portafolio.context_processors.categorias_disponibles',
            ],
        },
    },
]

# -------------------------
# Database
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------
# Internacionalización
# -------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('English')),
    ('it', _('Italiano')),
    ('de', _('Deutsch')),
    ('nl', _('Nederlands')),
    ('pt', _('Português')),
    ('fr', _('Français')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# -------------------------
# Static files
# -------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'portafolio' / 'static']

# -------------------------
# Cloudinary / Media
# -------------------------
# Usar variables de entorno exportadas o definidas en Render
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', '').strip(),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '').strip(),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', '').strip(),
}

# Determinar si Cloudinary está configurado
CLOUDINARY_CONFIGURED = all(CLOUDINARY_STORAGE.values())

if CLOUDINARY_CONFIGURED:
    # Subir archivos a Cloudinary
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = f'https://res.cloudinary.com/{CLOUDINARY_STORAGE["CLOUD_NAME"]}/image/upload/'
else:
    # Desarrollo local: guardar en /media
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------
# Default PK
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------
# Debug info (opcional, solo para verificar)
# -------------------------
if DEBUG:
    print("DEBUG INFO - Storage activo:", DEFAULT_FILE_STORAGE)
    print("DEBUG INFO - MEDIA_URL:", MEDIA_URL)
    print("DEBUG INFO - Cloudinary configurado:", CLOUDINARY_CONFIGURED)
