from portafolio.models import Category  # Cambiar Categoria por Category

def categorias_disponibles(request):
    """
    Context processor seguro para producción:
    Devuelve las categorías si existen, o lista vacía si hay algún error.
    """
    try:
        categorias = Category.objects.all()  # Cambiar Categoria por Category
    except Exception:
        # Si la DB no existe, no hay migraciones, o falla la consulta
        categorias = []

    return {'categories': categorias}  # Cambiar 'categorias' por 'categories'