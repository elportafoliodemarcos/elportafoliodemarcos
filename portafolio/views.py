from django.shortcuts import render, get_object_or_404
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
# Contacto (solo formulario interno, sin Mailjet)
# -------------------------
def contacto(request):
    mensaje_enviado = False
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")
        # Aquí podrías guardar el mensaje en DB o enviarlo a tu email usando otra forma
        mensaje_enviado = True  # Solo para indicar que se envió
    return render(request, 'portafolio/contacto.html', {'mensaje_enviado': mensaje_enviado})

# -------------------------
# Colaboración
# -------------------------
def colaboracion(request):
    opciones = [0.5, 5, 10, 20]
    mensaje_enviado = None
    tarjeta_enviada = None

    if request.method == "POST":
        monto = request.POST.get("monto")
        tarjeta = request.POST.get("tarjeta")
        if monto:
            try:
                mensaje_enviado = float(monto)
            except ValueError:
                mensaje_enviado = monto
            tarjeta_enviada = tarjeta

    return render(request, 'portafolio/colaboracion.html', {
        'opciones': opciones,
        'mensaje_enviado': mensaje_enviado,
        'tarjeta_enviada': tarjeta_enviada,
    })
