import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# -------------------------
# BASE
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "clave-local")

DEBUG = True

ALLOWED_HOSTS = [
    "elportafoliodemarcos.onrender.com",
    "localhost",
    "127.0.0.1",
]

# -------------------------
# APPS
# -------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # App
    "portafolio",
]

# -------------------------
# MIDDLEWARE
# -------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myportafolio.urls"
WSGI_APPLICATION = "myportafolio.wsgi.application"

# -------------------------
# TEMPLATES
# -------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "portafolio" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "portafolio.context_processors.categorias_disponibles",
            ],
        },
    },
]

# -------------------------
# DATABASE
# -------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -------------------------
# I18N
# -------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("es", _("Español")),
    ("en", _("English")),
    ("it", _("Italiano")),
    ("de", _("Deutsch")),
    ("nl", _("Nederlands")),
    ("pt", _("Português")),
    ("fr", _("Français")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# -------------------------
# STATIC FILES
# -------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "portafolio" / "static"]

# =========================================================
# 🔥 CLOUDINARY (CORREGIDO)
# =========================================================
# Eliminamos cloudinary.config() y usamos cloudinary_storage directamente
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME", "dfuypc2jq"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY", "699389243387785"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET", "TjOJg4K-w65zGmr0Hks5P4N6z58"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# -------------------------
# DEFAULT PK
# -------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
# Email (Mailjet)
# ==============================
from mailjet_rest import Client

MAILJET_API_KEY = os.environ.get("EMAIL_HOST_USER")        # clave pública
MAILJET_API_SECRET = os.environ.get("EMAIL_HOST_PASSWORD") # clave privada
DEFAULT_FROM_EMAIL = "elportafoliodemarcos@gmail.com"
CONTACT_EMAIL = DEFAULT_FROM_EMAIL

# Backend de Mailjet
if MAILJET_API_KEY and MAILJET_API_SECRET:
    EMAIL_BACKEND = "portafolio.mailjet_backend.MailjetBackend"
else:
    # Si faltan claves en dev, usar consola
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    if DEBUG:
        print("⚠️ DEBUG: Emails se mostrarán en consola, no se enviarán")
import cloudinary

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=CLOUDINARY_STORAGE["API_KEY"],
    api_secret=CLOUDINARY_STORAGE["API_SECRET"],
    secure=True
)
