from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Photo, Category
import requests
import json

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
# Función de ayuda para enviar email via Mailjet API
# -------------------------
def enviar_mailjet(nombre, email, mensaje):
    url = "https://api.mailjet.com/v3.1/send"
    data = {
        "Messages": [
            {
                "From": {"Email": settings.DEFAULT_FROM_EMAIL, "Name": "El Portafolio de Marcos"},
                "To": [{"Email": settings.DEFAULT_FROM_EMAIL, "Name": "Marcos"}],
                "Subject": f"Nuevo mensaje de contacto de {nombre}",
                "TextPart": f"De: {nombre} <{email}>\n\nMensaje:\n{mensaje}",
            }
        ]
    }
    try:
        response = requests.post(
            url,
            auth=(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD),
            json=data,
            timeout=15  # tiempo de espera seguro
        )
        response.raise_for_status()  # lanza excepción si status != 2xx
        return response
    except requests.exceptions.RequestException as e:
        # Mostramos el error completo en consola
        print("ERROR enviando email via Mailjet:", e)
        print("Payload enviado:", json.dumps(data, indent=2))
        return None

# -------------------------
# Contacto
# -------------------------
def contacto(request):
    mensaje_enviado = False
    error_envio = None

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")

        try:
            resp = enviar_mailjet(nombre, email, mensaje)
            if resp and resp.status_code == 200:
                mensaje_enviado = True
            else:
                error_envio = "Ocurrió un error enviando el email. Revisa la consola para más detalles."
        except Exception as e:
            error_envio = str(e)

    return render(request, 'portafolio/contacto.html', {
        'mensaje_enviado': mensaje_enviado,
        'error_envio': error_envio,
    })

# -------------------------
# Colaboración / Donativos
# -------------------------
def colaboracion(request):
    opciones = [0.5, 5, 10, 20]  # opciones de donativo
    mensaje_enviado = None
    tarjeta_enviada = None

    if request.method == "POST":
        tarjeta_enviada = request.POST.get("tarjeta")
        monto = request.POST.get("monto")
        mensaje_enviado = monto  # solo mostramos el monto en la página, puedes añadir lógica de pago real

    return render(request, 'portafolio/colaboracion.html', {
        'opciones': opciones,
        'mensaje_enviado': mensaje_enviado,
        'tarjeta_enviada': tarjeta_enviada,
    })
