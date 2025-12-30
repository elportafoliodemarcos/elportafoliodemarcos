#!/usr/bin/env python
"""
Script para verificar la configuración de Cloudinary en Render
Ejecutar en Render: python manage.py shell < check_render_cloudinary.py
O ejecutar directamente: python check_render_cloudinary.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportafolio.settings')
django.setup()

from django.conf import settings
from portafolio.models import Photo

print("=" * 70)
print("DIAGNÓSTICO DE CLOUDINARY EN RENDER")
print("=" * 70)

# 1. Verificar Storage
print("\n1. STORAGE CONFIGURADO:")
print(f"   {settings.DEFAULT_FILE_STORAGE}")
if 'cloudinary' in settings.DEFAULT_FILE_STORAGE.lower():
    print("   ✓ Cloudinary está ACTIVO")
else:
    print("   ✗ Cloudinary NO está activo - usando almacenamiento local")
    print("   → PROBLEMA: Las fotos se guardan localmente, no en Cloudinary")

# 2. Verificar variables de entorno
print("\n2. VARIABLES DE ENTORNO:")
cloud_name = settings.CLOUDINARY_CLOUD_NAME
api_key = settings.CLOUDINARY_API_KEY
api_secret = settings.CLOUDINARY_API_SECRET

print(f"   CLOUDINARY_CLOUD_NAME: '{cloud_name}' {'✓' if cloud_name else '✗'}")
print(f"   CLOUDINARY_API_KEY: '{api_key[:10] if api_key else 'VACÍO'}...' {'✓' if api_key else '✗'}")
print(f"   CLOUDINARY_API_SECRET: {'Configurado ✓' if api_secret else 'VACÍO ✗'}")

if not cloud_name or not api_key or not api_secret:
    print("\n   ⚠ PROBLEMA DETECTADO:")
    print("   → Las variables de entorno NO están configuradas en Render")
    print("   → Ve a Render Dashboard → Environment")
    print("   → Agrega las variables de Cloudinary")
    print("   → Asegúrate de que NO tengan espacios al inicio/final")

# 3. Verificar Cloudinary SDK
print("\n3. CLOUDINARY SDK:")
try:
    import cloudinary
    config = cloudinary.config()
    print(f"   Cloud Name: {config.cloud_name}")
    print(f"   API Key: {config.api_key[:10] if config.api_key else 'No configurado'}...")
    print("   ✓ Cloudinary SDK configurado")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# 4. Verificar fotos
print("\n4. FOTOS EN LA BASE DE DATOS:")
fotos = Photo.objects.all()
print(f"   Total: {fotos.count()}")

if fotos.count() > 0:
    foto = fotos.first()
    print(f"\n   Primera foto: {foto.title}")
    try:
        url = foto.image.url
        print(f"   URL: {url}")
        if 'cloudinary' in url:
            print("   ✓ URL de Cloudinary")
        else:
            print("   ✗ URL local (no funciona en Render)")
            print("   → La foto se guardó localmente, no en Cloudinary")
    except Exception as e:
        print(f"   ❌ Error obteniendo URL: {str(e)}")
else:
    print("   No hay fotos en la base de datos")

# 5. Resumen y recomendaciones
print("\n" + "=" * 70)
print("RESUMEN Y RECOMENDACIONES:")
print("=" * 70)

if 'cloudinary' not in settings.DEFAULT_FILE_STORAGE.lower():
    print("\n❌ PROBLEMA PRINCIPAL:")
    print("   Cloudinary NO está activo en Render")
    print("\n✅ SOLUCIÓN:")
    print("   1. Ve a Render Dashboard → tu servicio → Environment")
    print("   2. Verifica que estas variables estén configuradas:")
    print("      - CLOUDINARY_CLOUD_NAME = elportafolio")
    print("      - CLOUDINARY_API_KEY = 699389243387785")
    print("      - CLOUDINARY_API_SECRET = TjOJg4K-w65zGmr0Hks5P4N6z58")
    print("   3. Asegúrate de que NO tengan espacios al inicio/final")
    print("   4. Guarda y haz un nuevo deploy")
    print("   5. Elimina la foto de prueba y súbela de nuevo")
elif not cloud_name or not api_key or not api_secret:
    print("\n❌ PROBLEMA:")
    print("   Variables de entorno no configuradas correctamente")
    print("\n✅ SOLUCIÓN:")
    print("   Configura las variables de entorno en Render (ver arriba)")
else:
    print("\n✓ Configuración parece correcta")
    print("   Si las fotos no se ven, verifica los logs de Render")

print("\n" + "=" * 70)

