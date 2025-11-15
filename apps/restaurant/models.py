from django.db import models
from django.urls import reverse_lazy
from django.core.validators import MinValueValidator
from decimal import Decimal
from typing import Any

# -------------------------------------------------------------------------
#   MODELOS BASE
# -------------------------------------------------------------------------


class BaseModel(models.Model):
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
    delete_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de eliminación",
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name="Eliminado",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    class Meta:
        abstract = True


class NamedModel(BaseModel):
    """
    Modelo base para entidades que tienen un nombre.
    Ejemplos: Categorías, Mesas, Platos, etc.
    """

    name = models.CharField(max_length=150, verbose_name="Nombre")

    class Meta:  # type: ignore[misc]
        abstract = True

    def __str__(self) -> str:
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

    class Meta:  # type: ignore[misc]
        verbose_name = "Etiqueta alimentaria"
        verbose_name_plural = "Etiquetas alimentarias"
        ordering = ["name"]


# -------------------------------------------------------------------------
#   MODELO CATEGORY
# -------------------------------------------------------------------------


class Category(NamedModel):
    """
    Categorías para clasificar platos.
    Ejemplos: Pastas, Postres, Entradas, Bebidas, Carnes, Ensaladas, etc.
    """

    class Meta:  # type: ignore[misc]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]


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
        upload_to="media/dishes/",
        blank=True,
        null=True,
        verbose_name="Imagen",
    )

    # Categoría del plato (Pastas, Postres, Entradas, etc.)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoría",
        related_name="dishes",
    )

    # Tags alimentarios (vegano, sin gluten, lactosa, mariscos, picante, etc.)
    tags = models.ManyToManyField(  # type: ignore[var-annotated]
        "FoodTag",
        blank=True,
        verbose_name="Etiquetas",
        related_name="dishes",
    )

    class Meta:  # type: ignore[misc]
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse_lazy("dish_detail", kwargs={"pk": self.pk})


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

    dishes = models.ManyToManyField(  # type: ignore[var-annotated]
        Dish,
        verbose_name="Platos",
        related_name="menus",
        blank=True,
    )

    class Meta:  # type: ignore[misc]
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse_lazy("menu_detail", kwargs={"pk": self.pk})


# -------------------------------------------------------------------------
#   MODELO TABLE
# -------------------------------------------------------------------------


class Table(NamedModel):
    """
    Modelo que representa una mesa en el sistema.
    Hereda de NamedModel para incluir nombre, timestamps y estado.
    """

    capacity = models.PositiveIntegerField(
        verbose_name="Capacidad",
        help_text="Número máximo de comensales que puede acomodar la mesa.",
        validators=[MinValueValidator(1)],
    )

    class Meta:  # type: ignore[misc]
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} (capacidad: {self.capacity})"


# -------------------------------------------------------------------------
#   MODELO RESERVATION
# -------------------------------------------------------------------------


class Reservation(BaseModel):
    """
    Modelo que representa una reserva en el sistema.
    Hereda de TimeStampedModel para incluir timestamps y estado.
    """

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name="Mesa",
        related_name="reservations",
    )

    customer_name = models.CharField(
        max_length=150,
        verbose_name="Nombre del cliente",
    )

    reservation_datetime = models.DateTimeField(
        verbose_name="Fecha y hora de la reserva",
    )

    number_of_guests = models.PositiveIntegerField(
        verbose_name="Número de comensales",
        validators=[MinValueValidator(1)],
    )

    class Meta:  # type: ignore[misc]
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-reservation_datetime"]

    def __str__(self) -> str:
        return f"Reserva de {self.customer_name} para {self.number_of_guests} en {self.table.name} el {self.reservation_datetime}"


# -------------------------------------------------------------------------
#   MODELO ORDER
# -------------------------------------------------------------------------


class Order(BaseModel):
    """
    Modelo que representa un pedido en el sistema.
    Hereda de TimeStampedModel para incluir timestamps y estado.
    """

    class OrderStatus(models.TextChoices):
        """Estados del pedido"""

        PENDING = "PENDING", "Pendiente"
        READY = "READY", "Listo"
        DELIVERED = "DELIVERED", "Entregado"

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name="Mesa",
        related_name="orders",
    )

    dishes = models.ManyToManyField(  # type: ignore[var-annotated]
        Dish,
        verbose_name="Platos",
        related_name="orders",
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Estado",
    )

    is_paid = models.BooleanField(
        default=False,
        verbose_name="Pagado",
    )

    customer_name = models.CharField(
        max_length=150,
        verbose_name="Nombre del cliente",
        help_text="Cliente que consume y puede ocupar múltiples mesas",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Monto total",
        help_text="Sumatoria de todos los platos del pedido",
    )

    class Meta:  # type: ignore[misc]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Pedido #{self.pk} - {self.customer_name} - Mesa {self.table.name} - ${self.total_amount}"

    def calculate_total(self) -> Decimal:
        """Calcula el total del pedido sumando los precios de todos los platos"""
        total = sum(dish.price for dish in self.dishes.all())  # type: ignore[misc]
        return Decimal(str(total))

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Guarda el pedido y actualiza el total si ya tiene platos"""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Si no es nuevo y tiene platos, actualizar el total
        if not is_new and self.dishes.exists():  # type: ignore[misc]
            self.total_amount = self.calculate_total()
            super().save(update_fields=["total_amount"])
