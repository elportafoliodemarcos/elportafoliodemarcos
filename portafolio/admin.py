from django.contrib import admin
from .models import Photo, Category

# -----------------------------
# Registro de Categorías
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')                # Mostrar nombre y slug
    prepopulated_fields = {"slug": ("name",)}     # Auto-generar slug desde nombre
    search_fields = ('name', 'description')       # Buscar por nombre o descripción

# -----------------------------
# Registro de Fotos
# -----------------------------
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_public', 'created_at')  # columnas visibles
    list_filter = ('is_public', 'created_at', 'category')                      # filtros
    search_fields = ('title', 'description')                                   # búsqueda
    ordering = ('-created_at',)                                                # ordenar por fecha descendente
    list_editable = ('is_public', 'price')                                     # editable desde lista
    autocomplete_fields = ('category',)                                        # para seleccionar categoría fácilmente
