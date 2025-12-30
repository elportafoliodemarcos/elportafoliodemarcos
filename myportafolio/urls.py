import os
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from portafolio import views

urlpatterns = [
    # Sistema de cambio de idioma de Django
    path('i18n/', include('django.conf.urls.i18n')),
]

# Rutas principales con soporte multilenguaje
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('acerca/', views.acerca, name='acerca'),
    path('galeria/', views.galeria, name='galeria'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
    path('colaboracion/', views.colaboracion, name='colaboracion'),
    path('contacto/', views.contacto, name='contacto'),
)

# Servir archivos media en desarrollo (solo cuando DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)