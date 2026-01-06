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
# 🔥🔥🔥 CLOUDINARY — ESTA ES LA PARTE CLAVE 🔥🔥🔥
# =========================================================

import cloudinary

cloudinary.config(
    # ⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇
    # 👉 ESTAS 3 CLAVES DEBEN EXISTIR EN RENDER
    # 👉 NO SE ESCRIBEN AQUÍ A MANO
    # 👉 Render las inyecta automáticamente
    # ⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
)

# ❌ NO DEFAULT_FILE_STORAGE
# ❌ NO MEDIA_URL
# ❌ NO MEDIA_ROOT
# CloudinaryField se encarga solo

# -------------------------
# DEFAULT PK
# -------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
# Email (Mailjet)
# ==============================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Servidor SMTP de Mailjet
EMAIL_HOST = "in-v3.mailjet.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Variables de entorno de Mailjet (en Render)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")  # clave pública
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")  # clave privada

# Validación mínima: si no están definidas, Django usará un backend dummy en dev
if DEBUG and (not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    print("⚠️ DEBUG: Emails se mostrarán en consola, no se enviarán")

# Desde qué correo se envían los emails (debe estar verificado en Mailjet)
DEFAULT_FROM_EMAIL = "elportafoliodemarcos@gmail.com"
CONTACT_EMAIL = DEFAULT_FROM_EMAIL
