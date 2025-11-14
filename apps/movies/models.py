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


# -------------------------------------------------------------------------
#   MODELO DISH
# -------------------------------------------------------------------------


class Dish(NamedModel):
    """
    Modelo que representa un plato en el sistema.
    Hereda de NamedModel para incluir nombre, timestamps y estado.
    """

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Precio",
    )

    image = models.ImageField(
        upload_to='media/dishes/',
        blank=True,
        null=True,
        verbose_name="Imagen",
    )

    # Tags alimentarios (vegano, sin gluten, lactosa, mariscos, picante, etc.)
    tags = models.ManyToManyField(
        'FoodTag',
        blank=True,
        verbose_name='Etiquetas',
        related_name='dishes',
    )

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_lazy('dish_detail', kwargs={'pk': self.pk}) 


# -------------------------------------------------------------------------
#   MODELO MENU
# -------------------------------------------------------------------------


class Menu(NamedModel):
    """
    Modelo que representa un menú en el sistema.
    Hereda de NamedModel para incluir nombre, timestamps y estado.
    """
    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    dishes = models.ManyToManyField(
        Dish,                    
        verbose_name="Platos",
        related_name='menus',
        blank=True,              
    )

    class Meta:
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_lazy('menu_detail', kwargs={'pk': self.pk})
