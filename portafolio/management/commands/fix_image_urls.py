"""
Comando de Django para verificar y corregir URLs de imágenes
Uso: python manage.py fix_image_urls
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from portafolio.models import Photo


class Command(BaseCommand):
    help = 'Verifica y corrige las URLs de las imágenes para usar Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("DIAGNÓSTICO DE CLOUDINARY"))
        self.stdout.write("=" * 60)

        # 1. Verificar configuración
        self.stdout.write("\n1. CONFIGURACIÓN:")
        self.stdout.write(f"   Storage: {settings.DEFAULT_FILE_STORAGE}")
        
        if 'cloudinary' not in settings.DEFAULT_FILE_STORAGE.lower():
            self.stdout.write(self.style.ERROR(
                "   ✗ Cloudinary NO está activo!"
            ))
            self.stdout.write(self.style.WARNING(
                "   → Verifica las variables de entorno en Render"
            ))
            return
        
        self.stdout.write(self.style.SUCCESS("   ✓ Cloudinary está activo"))

        # 2. Verificar variables
        self.stdout.write("\n2. VARIABLES DE ENTORNO:")
        cloud_name = settings.CLOUDINARY_CLOUD_NAME
        api_key = settings.CLOUDINARY_API_KEY
        
        if not cloud_name or not api_key:
            self.stdout.write(self.style.ERROR(
                "   ✗ Variables de entorno no configuradas"
            ))
            return
        
        self.stdout.write(f"   Cloud Name: {cloud_name}")
        self.stdout.write(f"   API Key: {api_key[:10]}...")

        # 3. Verificar fotos
        self.stdout.write("\n3. FOTOS EN LA BASE DE DATOS:")
        fotos = Photo.objects.all()
        self.stdout.write(f"   Total: {fotos.count()}")

        cloudinary_count = 0
        local_count = 0

        for foto in fotos:
            try:
                url = foto.image.url
                if 'cloudinary' in url:
                    cloudinary_count += 1
                else:
                    local_count += 1
                    self.stdout.write(self.style.WARNING(
                        f"   ✗ {foto.title}: URL local"
                    ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"   ❌ {foto.title}: Error - {str(e)}"
                ))

        self.stdout.write(f"\n   ✓ Cloudinary: {cloudinary_count}")
        self.stdout.write(f"   ✗ Local: {local_count}")

        # 4. Recomendaciones
        self.stdout.write("\n4. RECOMENDACIONES:")
        if local_count > 0:
            self.stdout.write(self.style.WARNING(
                f"   ⚠ Hay {local_count} fotos con URLs locales"
            ))
            self.stdout.write(
                "   → Elimina las fotos desde el admin y súbelas de nuevo"
            )
            self.stdout.write(
                "   → O ejecuta: python manage.py migrate_images_to_cloudinary"
            )
        else:
            self.stdout.write(self.style.SUCCESS(
                "   ✓ Todas las fotos están en Cloudinary"
            ))

        self.stdout.write("\n" + "=" * 60)

