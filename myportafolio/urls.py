import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns  # ✅ Importante para URLs con idioma
from portafolio import views

urlpatterns = [
    # Ruta para el sistema de cambio de idioma de Django
    path('i18n/', include('django.conf.urls.i18n')),
]

# ✅ Rutas principales con soporte multilenguaje
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('acerca/', views.acerca, name='acerca'),
    path('galeria/', views.galeria, name='galeria'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
    path('colaboracion/', views.colaboracion, name='colaboracion'),
    path('contacto/', views.contacto, name='contacto'),
)

# ✅ Archivos estáticos y multimedia (sin cambios)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'portafolio/static'))
