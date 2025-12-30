from .models import Category

def categorias_disponibles(request):
    try:
        categorias = Category.objects.all()
    except Exception:
        categorias = []
    return {
        'categorias_disponibles': categorias
    }
