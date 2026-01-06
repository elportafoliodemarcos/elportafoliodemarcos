from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from portafolio import views

# URLs fuera de i18n
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs con soporte multilenguaje
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('acerca/', views.acerca, name='acerca'),
    path('galeria/', views.galeria, name='galeria'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
    path('colaboracion/', views.colaboracion, name='colaboracion'),  # <-- agregada
    path('contacto/', views.contacto, name='contacto'),
)
