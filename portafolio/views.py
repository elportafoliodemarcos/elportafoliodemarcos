from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Photo, Category

# -------------------------
# Página de inicio
# -------------------------
def home(request):
    featured_photos = Photo.objects.filter(is_featured=True, image__isnull=False)[:5]
    category_photos = {category: Photo.objects.filter(category=category, image__isnull=False) 
                       for category in Category.objects.all()}
    donativo_opciones = [0.5, 5, 10, 20]

    context = {
        'featured_photos': featured_photos,
        'category_photos': category_photos,
        'donativo_opciones': donativo_opciones,
    }
    return render(request, 'portafolio/home.html', context)

# -------------------------
# Galería completa
# -------------------------
def galeria(request):
    fotos = Photo.objects.filter(image__isnull=False)
    banners = Photo.objects.filter(is_featured=True, image__isnull=False)[:5]  # carousel opcional
    return render(request, 'portafolio/galeria.html', {'fotos': fotos, 'banners': banners})

# -------------------------
# Galería por categoría
# -------------------------
def categoria(request, slug):
    category = get_object_or_404(Category, slug=slug)
    photos = Photo.objects.filter(category=category, image__isnull=False)
    return render(request, 'portafolio/categoria.html', {'category': category, 'photos': photos})

# -------------------------
# Acerca de
# -------------------------
def acerca(request):
    acerca_texto = "Aquí va tu texto de presentación..."
    return render(request, 'portafolio/acerca.html', {'texto': acerca_texto})

# -------------------------
# Contacto (con Mailjet)
# -------------------------
def contacto(request):
    mensaje_enviado = False
    error_envio = None

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")

        asunto = f"Nuevo mensaje de contacto de {nombre}"
        mensaje_completo = f"De: {nombre} <{email}>\n\nMensaje:\n{mensaje}"

        try:
            send_mail(
                asunto,
                mensaje_completo,
                settings.DEFAULT_FROM_EMAIL,           # remitente (verificado en Mailjet)
                [settings.DEFAULT_FROM_EMAIL],         # destinatario (tu correo)
                fail_silently=False
            )
            mensaje_enviado = True
        except Exception as e:
            error_envio = str(e)
            mensaje_enviado = False

    return render(request, 'portafolio/contacto.html', {
        'mensaje_enviado': mensaje_enviado,
        'error_envio': error_envio,
    })
