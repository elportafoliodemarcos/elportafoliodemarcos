# portafolio/scripts/export_to_cloudinary.py
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportafolio.settings')
django.setup()

from portafolio.models import Photo

def main():
    photos = Photo.objects.filter(image='')  # Solo las que no tienen Cloudinary
    for photo in photos:
        print(f"Subiendo {photo.title} a Cloudinary...")
        # Al guardar el modelo, Cloudinary se encargará de subirlo
        photo.save()
    print("✅ Todas las fotos subidas a Cloudinary.")

if __name__ == "__main__":
    main()