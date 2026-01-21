from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from .models import Photo, Category
import requests
import os

# -------------------------
# Página de inicio
# -------------------------
def home(request):
    featured_photos = Photo.objects.filter(is_featured=True).order_by('-created_at')[:5]
    category_photos = {
        category: Photo.objects.filter(category=category, image__isnull=False)
        for category in Category.objects.all()
    }
    donativo_opciones = [0.5, 5, 10, 20]

    return render(request, 'portafolio/home.html', {
        'featured_photos': featured_photos,
        'category_photos': category_photos,
        'donativo_opciones': donativo_opciones,
    })

# -------------------------
# Galería completa
# -------------------------
def galeria(request):
    fotos = Photo.objects.filter(image__isnull=False)
    banners = Photo.objects.filter(is_featured=True, image__isnull=False)[:5]
    return render(request, 'portafolio/galeria.html', {
        'fotos': fotos,
        'banners': banners
    })

# -------------------------
# Galería por categoría
# -------------------------
def categoria(request, slug):
    category = get_object_or_404(Category, slug=slug)
    photos = Photo.objects.filter(category=category, image__isnull=False)
    return render(request, 'portafolio/categoria.html', {
        'category': category,
        'photos': photos
    })

# -------------------------
# Acerca de
# -------------------------
def acerca(request):
    return render(request, 'portafolio/acerca.html', {
        'texto': "Aquí va tu texto de presentación..."
    })

# -------------------------
# Envío de email con Mailjet API
# -------------------------
def enviar_mailjet(nombre, email, mensaje):
    url = "https://api.mailjet.com/v3.1/send"
    data = {
        "Messages": [
            {
                "From": {
                    "Email": settings.DEFAULT_FROM_EMAIL,
                    "Name": "El Portafolio de Marcos"
                },
                "To": [
                    {
                        "Email": settings.CONTACT_EMAIL,
                        "Name": "Marcos"
                    }
                ],
                "Subject": f"Nuevo mensaje de contacto de {nombre}",
                "TextPart": f"De: {nombre} <{email}>\n\nMensaje:\n{mensaje}",
            }
        ]
    }
    return requests.post(
        url,
        auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET),
        json=data,
        timeout=10
    )

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
            if resp.status_code in (200, 201):
                mensaje_enviado = True
            else:
                error_envio = f"Error Mailjet ({resp.status_code})"
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
    opciones = [0.5, 5, 10, 20]
    mensaje_enviado = None
    tarjeta_enviada = None

    if request.method == "POST":
        tarjeta_enviada = request.POST.get("tarjeta")
        mensaje_enviado = request.POST.get("monto")

    return render(request, 'portafolio/colaboracion.html', {
        'opciones': opciones,
        'mensaje_enviado': mensaje_enviado,
        'tarjeta_enviada': tarjeta_enviada,
    })

# -------------------------
# Descarga de foto compatible Local / Render
# -------------------------
def descargar_foto(request, pk):
    foto = get_object_or_404(Photo, pk=pk)
    if not foto.image:
        return HttpResponse("No hay imagen disponible", status=404)

    filename = foto.title.replace(" ", "_")

    # Si estamos en local (DEBUG=True) usamos StreamingHttpResponse
    if settings.DEBUG:
        try:
            r = requests.get(foto.image.url, stream=True)
            if r.status_code != 200:
                return HttpResponse("Error descargando la imagen", status=500)

            response = StreamingHttpResponse(r.iter_content(1024), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{filename}.jpg"'
            return response
        except requests.RequestException:
            return HttpResponse("Error descargando la imagen", status=500)

    # En producción (Render), redirigimos a Cloudinary con fl_attachment
    else:
        download_url = f"{foto.image.url}?fl_attachment&filename={filename}.jpg"
        return HttpResponse(f'<script>window.location="{download_url}";</script>')
