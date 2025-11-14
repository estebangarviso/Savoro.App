from django.db import models
from django.urls import reverse_lazy

# -------------------------------------------------------------------------
#   MODELOS BASE
# -------------------------------------------------------------------------

class TimeStampedModel(models.Model):
    """
    Modelo base genérico con fechas y estado.
    Útil para cualquier entidad del sistema: reservas, pedidos, platos, mesas, etc.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    class Meta:
        abstract = True


class NamedModel(TimeStampedModel):
    """
    Modelo base para entidades que tienen un nombre.
    Ejemplos: Categorías, Mesas, Platos, etc.
    """
    name = models.CharField(max_length=150, verbose_name="Nombre")

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

# -------------------------------------------------------------------------
#   MODELO FOOD TAG
# -------------------------------------------------------------------------

class FoodTag(NamedModel):
    """
    Etiquetas alimentarias para clasificar platos.
    Pueden ser alérgenos, tipos de dieta, características o restricciones.
    Ejemplos: Vegano, Sin Gluten, Mariscos, Picante, Maní, Lactosa, etc.
    """
    class Meta:
        verbose_name = "Etiqueta alimentaria"
        verbose_name_plural = "Etiquetas alimentarias"
        ordering = ['name']

# -------------------------------------------------------------------------
#   MODELO CATEGORY
# -------------------------------------------------------------------------

class Category(NamedModel):
    """
    Categorías para clasificar platos.
    Ejemplos: Pastas, Postres, Entradas, Bebidas, Carnes, Ensaladas, etc.
    """
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']





class Movies(BaseName):
    description = models.CharField(max_length=256, verbose_name="Descripcion")
    image = models.ImageField(upload_to="movies", verbose_name="Imagen")
    release_date = models.DateField(verbose_name="Fecha de publicacion")
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, verbose_name="Categoria"
    )

    class Meta:
        verbose_name = "Pelicula"
        verbose_name_plural = "Peliculas"

    def get_edit_url(self):
        return reverse_lazy("movies:movies-edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("movies:movies-delete", kwargs={"pk": self.pk})

    def get_detail_url(self):
        return reverse_lazy("movies:movies-detail", kwargs={"pk": self.pk})
