import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# -------------------------
# Rutas y seguridad
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'tu-secreto-local')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    "elportafoliodemarcos.onrender.com",
    "localhost",
    "127.0.0.1"
]

# -------------------------
# Apps instaladas
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
# Templates y context processors
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
                # Context processor seguro
                'portafolio.context_processors.categorias_disponibles',
            ],
        },
    },
]

# -------------------------
# Base de datos (SQLite)
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------
# Contraseñas
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

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

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# -------------------------
# Archivos estáticos y multimedia
# -------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'portafolio/static')]

# Configuración de Media Files (para desarrollo local)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------
# Cloudinary (solo si está configurado)
# -------------------------
# Obtener variables de entorno y eliminar espacios en blanco
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "").strip()
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "").strip()

# Verificar si Cloudinary está configurado (todas las variables deben tener valor)
CLOUDINARY_CONFIGURED = bool(
    CLOUDINARY_CLOUD_NAME and 
    CLOUDINARY_API_KEY and 
    CLOUDINARY_API_SECRET
)

if CLOUDINARY_CONFIGURED:
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
        )
        DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
        
        # Log para verificar en producción (solo si DEBUG está activo)
        if DEBUG:
            print(f"✓ Cloudinary configurado: {CLOUDINARY_CLOUD_NAME}")
    except Exception as e:
        # Si hay error al configurar Cloudinary, usar almacenamiento local
        if DEBUG:
            print(f"⚠ Error configurando Cloudinary: {str(e)}")
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
        CLOUDINARY_CONFIGURED = False
else:
    # En desarrollo local sin Cloudinary, usar almacenamiento local
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    if DEBUG:
        print("⚠ Cloudinary no configurado, usando almacenamiento local")

# Para Django 5+
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'