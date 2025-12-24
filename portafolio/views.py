from django.shortcuts import render, get_object_or_404
from .models import Photo, Category
from mailjet_rest import Client # type: ignore
from django.conf import settings

# -------------------------
# Página de inicio
# -------------------------
def home(request):
    featured_photos = Photo.objects.filter(is_featured=True)[:5]
    category_photos = {category: Photo.objects.filter(category=category) for category in Category.objects.all()}
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
    photos = Photo.objects.all()
    return render(request, 'portafolio/galeria.html', {'photos': photos})

# -------------------------
# Galería por categoría
# -------------------------
def categoria(request, slug):
    category = get_object_or_404(Category, slug=slug)
    photos = Photo.objects.filter(category=category)
    return render(request, 'portafolio/categoria.html', {'category': category, 'photos': photos})

# -------------------------
# Acerca de
# -------------------------
def acerca(request):
    acerca_texto = """
    Mi nombre es Marcos, soy uruguayo, nacido en el barrio La Blanqueada de Montevideo, 
    y desde muy joven encontré en la fotografía una forma de detener el tiempo y observar la vida con atención y sensibilidad. 
    Este proyecto nace del deseo de compartir cómo percibo el mundo: desde lo cotidiano, en sus pequeños gestos y detalles, 
    hasta lo inesperado, los instantes singulares que a menudo pasan desapercibidos pero que encierran historias propias. 
    Cada fotografía es un fragmento de realidad, un instante detenido que busca transmitir emociones y sensaciones a quienes lo contemplan.

    Mi mirada se nutre de la curiosidad por entender cómo los seres humanos interactuamos con nuestro entorno y por descubrir 
    las múltiples formas en que la vida se manifiesta. Lo que para algunos puede parecer trivial, para mí se convierte en motivo de fascinación; 
    y lo extraordinario, cuando aparece, es capturado con respeto y asombro. En este espacio comparto no solo imágenes, sino también reflexiones visuales 
    y experiencias que invitan a observar el mundo desde otra perspectiva.

    Aunque me considero un fotógrafo amateur, abordo mi trabajo con dedicación y cuidado, buscando siempre transmitir autenticidad. 
    Creo profundamente que la fotografía, como forma de arte, debería ser accesible para todos. Por ello, he decidido que mi trabajo esté disponible gratuitamente, 
    con la opción de apoyar mediante colaboraciones voluntarias quienes deseen y puedan contribuir. Esta modalidad me permite continuar creando con libertad, 
    manteniendo la independencia de mi visión artística, sin imponer barreras económicas al acceso a las imágenes.
    """
    return render(request, 'portafolio/acerca.html', {'texto': acerca_texto})

# -------------------------
# Contacto usando Mailjet
# -------------------------
def contacto(request):
    mensaje_enviado = False
    error_envio = None

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")

        mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": settings.DEFAULT_FROM_EMAIL,
                        "Name": "Portafolio de Marcos"
                    },
                    "To": [
                        {
                            "Email": "elportafoliodemarcos@gmail.com",
                            "Name": "Marcos"
                        }
                    ],
                    "Subject": f"Nuevo mensaje de {nombre}",
                    "TextPart": f"De: {nombre} <{email}>\n\n{mensaje}",
                    "HTMLPart": f"<h4>De: {nombre} &lt;{email}&gt;</h4><p>{mensaje}</p>"
                }
            ]
        }

        try:
            result = mailjet.send.create(data=data)
            if result.status_code == 200:
                mensaje_enviado = True
            else:
                error_envio = f"Ocurrió un error al enviar: {result.status_code}"
        except Exception as e:
            error_envio = str(e)

    context = {
        'mensaje_enviado': mensaje_enviado,
        'error_envio': error_envio
    }
    return render(request, 'portafolio/contacto.html', context)

# -------------------------
# Colaboración (antes Donativos)
# -------------------------
def colaboracion(request):
    opciones = [0.5, 5, 10, 20]  # montos sugeridos
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

    context = {
        'opciones': opciones,
        'mensaje_enviado': mensaje_enviado,
        'tarjeta_enviada': tarjeta_enviada,
    }
    return render(request, 'portafolio/colaboracion.html', context)
    