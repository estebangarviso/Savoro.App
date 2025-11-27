"""
Seed data command - Populate database with initial data
"""

from __future__ import annotations

from typing import Any
from decimal import Decimal

from django.core.management.base import BaseCommand

from modules.category.models import Category
from modules.dish.models import Dish
from modules.food_tag.models import FoodTag


class Command(BaseCommand):
    help = "Poblar la base de datos con datos iniciales del restaurante"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        self.stdout.write("Iniciando población de datos...")

        # Limpiar datos existentes
        self.stdout.write("Limpiando datos existentes...")
        Dish.objects.all().delete()
        Category.objects.all().delete()
        FoodTag.objects.all().delete()

        # Crear etiquetas alimentarias
        self.stdout.write("Creando etiquetas alimentarias...")
        tags = self._create_food_tags()

        # Crear categorías
        self.stdout.write("Creando categorías...")
        categories = self._create_categories()

        # Crear platos
        self.stdout.write("Creando platos...")
        dishes = self._create_dishes(tags, categories)

        self.stdout.write(self.style.SUCCESS("¡Datos poblados exitosamente!"))
        self.stdout.write(f"  - {len(tags)} etiquetas alimentarias")
        self.stdout.write(f"  - {len(categories)} categorías")
        self.stdout.write(f"  - {len(dishes)} platos")

    def _create_food_tags(self) -> list[FoodTag]:
        """Crear etiquetas alimentarias"""
        tags_data = [
            "Vegano",
            "Vegetariano",
            "Sin Gluten",
            "Sin Lactosa",
            "Picante",
            "Mariscos",
            "Maní",
            "Frutos Secos",
            "Huevo",
            "Soya",
            "Orgánico",
            "Bajo en Calorías",
        ]
        tags = []
        for tag_name in tags_data:
            tag, _ = FoodTag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        return tags

    def _create_categories(self) -> list[Category]:
        """Crear categorías de platos"""
        categories_data = [
            "Entradas",
            "Ensaladas",
            "Sopas",
            "Pastas",
            "Carnes",
            "Pescados y Mariscos",
            "Pizzas",
            "Postres",
            "Bebidas",
            "Vinos",
        ]
        categories = []
        for cat_name in categories_data:
            category, _ = Category.objects.get_or_create(name=cat_name)
            categories.append(category)
        return categories

    def _create_dishes(
        self, tags: list[FoodTag], categories: list[Category]
    ) -> list[Dish]:
        """Crear platos con sus etiquetas y categorías"""
        # Índices de tags: 0=Vegano, 1=Vegetariano, 2=Sin Gluten, 3=Sin Lactosa,
        #          4=Picante, 5=Mariscos, 6=Maní, 7=Frutos Secos,
        #          8=Huevo, 9=Soya, 10=Orgánico, 11=Bajo en Calorías
        # Categorías: 0=Entradas, 1=Ensaladas, 2=Sopas, 3=Pastas, 4=Carnes,
        #             5=Pescados y Mariscos, 6=Pizzas, 7=Postres, 8=Bebidas, 9=Vinos

        dishes_data = [
            # Entradas
            {
                "name": "Empanadas de Carne",
                "description": "Deliciosas empanadas rellenas de carne molida, cebolla y especias tradicionales",
                "price": Decimal("4500.00"),
                "category": 0,
                "tags": [],
            },
            {
                "name": "Tabla de Quesos",
                "description": "Selección de quesos artesanales con mermelada de higos y frutos secos",
                "price": Decimal("8900.00"),
                "category": 0,
                "tags": [1, 7],
            },
            {
                "name": "Ceviche de Pescado",
                "description": "Pescado fresco marinado en limón con cebolla morada, cilantro y ají",
                "price": Decimal("9500.00"),
                "category": 0,
                "tags": [2, 4],
            },
            {
                "name": "Bruschetta Caprese",
                "description": "Pan tostado con tomate, mozzarella fresca, albahaca y aceite de oliva",
                "price": Decimal("5200.00"),
                "category": 0,
                "tags": [1],
            },
            # Ensaladas
            {
                "name": "Ensalada César",
                "description": "Lechuga romana, crutones, parmesano y aderezo César casero",
                "price": Decimal("6800.00"),
                "category": 1,
                "tags": [8],
            },
            {
                "name": "Ensalada Mediterránea",
                "description": "Mix de lechugas, tomate, pepino, aceitunas, queso feta y vinagreta",
                "price": Decimal("7200.00"),
                "category": 1,
                "tags": [1, 2],
            },
            {
                "name": "Ensalada Vegana Bowl",
                "description": "Quinoa, garbanzos, aguacate, tomates cherry, espinaca y tahini",
                "price": Decimal("7900.00"),
                "category": 1,
                "tags": [0, 2, 10],
            },
            # Sopas
            {
                "name": "Cazuela de Vacuno",
                "description": "Tradicional sopa chilena con carne de vacuno, zapallo, choclo y papas",
                "price": Decimal("8500.00"),
                "category": 2,
                "tags": [],
            },
            {
                "name": "Crema de Zapallo",
                "description": "Suave crema de zapallo con jengibre y crema de leche",
                "price": Decimal("5800.00"),
                "category": 2,
                "tags": [1],
            },
            # Pastas
            {
                "name": "Fetuccini Alfredo",
                "description": "Pasta fresca con salsa cremosa de parmesano y mantequilla",
                "price": Decimal("9800.00"),
                "category": 3,
                "tags": [1],
            },
            {
                "name": "Espagueti Boloñesa",
                "description": "Pasta con salsa de carne molida, tomate y hierbas italianas",
                "price": Decimal("10500.00"),
                "category": 3,
                "tags": [],
            },
            {
                "name": "Ravioles de Espinaca y Ricotta",
                "description": "Ravioles rellenos de espinaca y ricotta con salsa de tomate albahaca",
                "price": Decimal("11200.00"),
                "category": 3,
                "tags": [1],
            },
            {
                "name": "Pasta Arrabiata",
                "description": "Penne con salsa de tomate picante, ajo y perejil",
                "price": Decimal("9200.00"),
                "category": 3,
                "tags": [1, 0, 4],
            },
            # Carnes
            {
                "name": "Bife de Chorizo",
                "description": "Jugoso bife de chorizo de 300g con papas rústicas y vegetales",
                "price": Decimal("15900.00"),
                "category": 4,
                "tags": [2],
            },
            {
                "name": "Lomo a la Pimienta",
                "description": "Medallones de lomo con salsa de pimienta verde y puré de papas",
                "price": Decimal("17500.00"),
                "category": 4,
                "tags": [],
            },
            {
                "name": "Costillar de Cerdo BBQ",
                "description": "Costillar de cerdo glaseado con salsa BBQ casera y ensalada coleslaw",
                "price": Decimal("14800.00"),
                "category": 4,
                "tags": [],
            },
            {
                "name": "Pollo al Limón",
                "description": "Pechuga de pollo con salsa de limón, alcaparras y arroz pilaf",
                "price": Decimal("11900.00"),
                "category": 4,
                "tags": [2, 11],
            },
            # Pescados y Mariscos
            {
                "name": "Salmón a la Plancha",
                "description": "Filete de salmón con espárragos y salsa de eneldo",
                "price": Decimal("16500.00"),
                "category": 5,
                "tags": [2, 11],
            },
            {
                "name": "Paella de Mariscos",
                "description": "Arroz con camarones, calamares, mejillones y azafrán",
                "price": Decimal("18900.00"),
                "category": 5,
                "tags": [5, 2],
            },
            {
                "name": "Corvina con Alcaparras",
                "description": "Filete de corvina con salsa de alcaparras, limón y papas al vapor",
                "price": Decimal("15200.00"),
                "category": 5,
                "tags": [2],
            },
            # Pizzas
            {
                "name": "Pizza Margherita",
                "description": "Salsa de tomate, mozzarella fresca, albahaca y aceite de oliva",
                "price": Decimal("9500.00"),
                "category": 6,
                "tags": [1],
            },
            {
                "name": "Pizza Pepperoni",
                "description": "Salsa de tomate, mozzarella y abundante pepperoni",
                "price": Decimal("10800.00"),
                "category": 6,
                "tags": [],
            },
            {
                "name": "Pizza Cuatro Quesos",
                "description": "Mozzarella, gorgonzola, parmesano y provolone",
                "price": Decimal("11500.00"),
                "category": 6,
                "tags": [1],
            },
            {
                "name": "Pizza Vegetariana",
                "description": "Champiñones, pimientos, cebolla, aceitunas y tomate",
                "price": Decimal("10200.00"),
                "category": 6,
                "tags": [1],
            },
            # Postres
            {
                "name": "Tiramisú",
                "description": "Clásico postre italiano con café, mascarpone y cacao",
                "price": Decimal("5500.00"),
                "category": 7,
                "tags": [1, 8],
            },
            {
                "name": "Cheesecake de Frutos Rojos",
                "description": "Tarta de queso con base de galleta y coulis de frutos rojos",
                "price": Decimal("5800.00"),
                "category": 7,
                "tags": [1],
            },
            {
                "name": "Brownie con Helado",
                "description": "Brownie de chocolate tibio con helado de vainilla y salsa de chocolate",
                "price": Decimal("5200.00"),
                "category": 7,
                "tags": [1, 7],
            },
            {
                "name": "Flan Casero",
                "description": "Flan tradicional con caramelo casero y crema chantilly",
                "price": Decimal("4200.00"),
                "category": 7,
                "tags": [1, 2],
            },
            # Bebidas
            {
                "name": "Limonada Natural",
                "description": "Limonada fresca con menta y hielo",
                "price": Decimal("2500.00"),
                "category": 8,
                "tags": [0, 2],
            },
            {
                "name": "Jugo Natural del Día",
                "description": "Jugo de frutas frescas de temporada",
                "price": Decimal("2800.00"),
                "category": 8,
                "tags": [0, 2],
            },
            {
                "name": "Café Espresso",
                "description": "Café espresso italiano",
                "price": Decimal("1800.00"),
                "category": 8,
                "tags": [0],
            },
        ]

        dishes: list[Dish] = []

        for dish_data in dishes_data:
            # Asignar categoría si existe
            category = None
            if "category" in dish_data and 0 <= dish_data["category"] < len(categories):
                category = categories[dish_data["category"]]

            dish = Dish.objects.create(
                name=dish_data["name"],
                description=dish_data["description"],
                price=dish_data["price"],
                category=category,
            )
            # Asignar tags usando los índices
            for tag_index in dish_data.get("tags", []):
                if 0 <= tag_index < len(tags):
                    dish.tags.add(tags[tag_index])
            dishes.append(dish)

        return dishes
