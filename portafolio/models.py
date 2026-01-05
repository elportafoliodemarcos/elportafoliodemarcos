from django.db import models

# Modelo de categoría
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# Modelo de foto (subida a Cloudinary)
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')  # Las imágenes se guardarán automáticamente en Cloudinary
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
        blank=True
    )
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
