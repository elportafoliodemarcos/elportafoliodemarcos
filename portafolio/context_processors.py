from .models import Category

def categorias_disponibles(request):
    """
    Devuelve todas las categorías para que siempre estén disponibles en templates.
    """
    return {
        'categories': Category.objects.all()
    }
