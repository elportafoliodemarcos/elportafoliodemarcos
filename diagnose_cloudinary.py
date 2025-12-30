#!/usr/bin/env python
"""
Script de diagnóstico para verificar la configuración de Cloudinary
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportafolio.settings')
django.setup()

from django.conf import settings
from portafolio.models import Photo

print("=" * 60)
print("DIAGNÓSTICO DE CLOUDINARY")
print("=" * 60)

# 1. Verificar variables de entorno
print("\n1. VARIABLES DE ENTORNO:")
print(f"   CLOUDINARY_CLOUD_NAME: '{settings.CLOUDINARY_CLOUD_NAME}'")
print(f"   CLOUDINARY_API_KEY: '{settings.CLOUDINARY_API_KEY[:10] if settings.CLOUDINARY_API_KEY else 'No configurado'}...'")
print(f"   CLOUDINARY_API_SECRET: {'Configurado' if settings.CLOUDINARY_API_SECRET else 'No configurado'}")

# 2. Verificar storage
print("\n2. STORAGE CONFIGURADO:")
print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
if 'cloudinary' in settings.DEFAULT_FILE_STORAGE.lower():
    print("   ✓ Cloudinary está activo")
else:
    print("   ✗ Cloudinary NO está activo - usando almacenamiento local")

# 3. Verificar si Cloudinary está configurado
print("\n3. CONFIGURACIÓN DE CLOUDINARY:")
try:
    import cloudinary
    print(f"   Cloud Name: {cloudinary.config().cloud_name}")
    print(f"   API Key: {cloudinary.config().api_key[:10]}...")
    print("   ✓ Cloudinary SDK configurado correctamente")
except Exception as e:
    print(f"   ✗ Error configurando Cloudinary: {str(e)}")

# 4. Verificar fotos en la base de datos
print("\n4. FOTOS EN LA BASE DE DATOS:")
fotos = Photo.objects.all()
print(f"   Total de fotos: {fotos.count()}")

cloudinary_count = 0
local_count = 0
error_count = 0

for foto in fotos[:5]:  # Solo las primeras 5
    try:
        url = foto.image.url
        if 'cloudinary' in url:
            cloudinary_count += 1
            print(f"   ✓ {foto.title[:30]:30} → Cloudinary")
        else:
            local_count += 1
            print(f"   ✗ {foto.title[:30]:30} → Local: {url[:50]}")
    except Exception as e:
        error_count += 1
        print(f"   ❌ {foto.title[:30]:30} → Error: {str(e)}")

if fotos.count() > 5:
    print(f"   ... y {fotos.count() - 5} más")

# 5. Resumen
print("\n5. RESUMEN:")
print(f"   Fotos con URLs de Cloudinary: {cloudinary_count}")
print(f"   Fotos con URLs locales: {local_count}")
print(f"   Fotos con errores: {error_count}")

# 6. Recomendaciones
print("\n6. RECOMENDACIONES:")
if 'cloudinary' not in settings.DEFAULT_FILE_STORAGE.lower():
    print("   ⚠ Cloudinary NO está activo")
    print("   → Verifica las variables de entorno en Render")
    print("   → Asegúrate de que no tengan espacios al inicio/final")
elif local_count > 0:
    print("   ⚠ Hay fotos con URLs locales")
    print("   → Las fotos necesitan ser re-subidas desde el admin")
    print("   → O ejecuta el script de migración")
else:
    print("   ✓ Todo parece estar configurado correctamente")

print("\n" + "=" * 60)

