from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.restaurant.models import (
    Category,
    Dish,
    Menu,
    Order,
    Reservation,
    Table,
    FoodTag,
)


class Command(BaseCommand):
    help = "Poblar la base de datos con datos iniciales del restaurante"

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando población de datos...")

        # Limpiar datos existentes
        self.stdout.write("Limpiando datos existentes...")
        Order.objects.all().delete()
        Reservation.objects.all().delete()
        Menu.objects.all().delete()
        Dish.objects.all().delete()
        Table.objects.all().delete()
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
        dishes = self._create_dishes(tags)

        # Crear menús
        self.stdout.write("Creando menús...")
        menus = self._create_menus(dishes)

        # Crear mesas
        self.stdout.write("Creando mesas...")
        tables = self._create_tables()

        # Crear reservas
        self.stdout.write("Creando reservas...")
        reservations = self._create_reservations(tables)

        # Crear pedidos
        self.stdout.write("Creando pedidos...")
        orders = self._create_orders(tables, dishes)

        self.stdout.write(self.style.SUCCESS("¡Datos poblados exitosamente!"))
        self.stdout.write(f"  - {len(tags)} etiquetas alimentarias")
        self.stdout.write(f"  - {len(categories)} categorías")
        self.stdout.write(f"  - {len(dishes)} platos")
        self.stdout.write(f"  - {len(menus)} menús")
        self.stdout.write(f"  - {len(tables)} mesas")
        self.stdout.write(f"  - {len(reservations)} reservas")
        self.stdout.write(f"  - {len(orders)} pedidos")

    def _create_food_tags(self):
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

    def _create_categories(self):
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

    def _create_dishes(self, tags):
        """Crear platos con sus etiquetas"""
        # Crear un diccionario de tags por id (índice en la lista + 1)
        # Índices: 0=Vegano, 1=Vegetariano, 2=Sin Gluten, 3=Sin Lactosa,
        #          4=Picante, 5=Mariscos, 6=Maní, 7=Frutos Secos,
        #          8=Huevo, 9=Soya, 10=Orgánico, 11=Bajo en Calorías

        dishes_data = [
            # Entradas
            {
                "name": "Empanadas de Carne",
                "description": "Deliciosas empanadas rellenas de carne molida, cebolla y especias tradicionales",
                "price": 4500.00,
                "tags": [],
            },
            {
                "name": "Tabla de Quesos",
                "description": "Selección de quesos artesanales con mermelada de higos y frutos secos",
                "price": 8900.00,
                "tags": [1, 7],  # Vegetariano, Frutos Secos
            },
            {
                "name": "Ceviche de Pescado",
                "description": "Pescado fresco marinado en limón con cebolla morada, cilantro y ají",
                "price": 9500.00,
                "tags": [2, 4],  # Sin Gluten, Picante
            },
            {
                "name": "Bruschetta Caprese",
                "description": "Pan tostado con tomate, mozzarella fresca, albahaca y aceite de oliva",
                "price": 5200.00,
                "tags": [1],  # Vegetariano
            },
            # Ensaladas
            {
                "name": "Ensalada César",
                "description": "Lechuga romana, crutones, parmesano y aderezo César casero",
                "price": 6800.00,
                "tags": [8],  # Huevo
            },
            {
                "name": "Ensalada Mediterránea",
                "description": "Mix de lechugas, tomate, pepino, aceitunas, queso feta y vinagreta",
                "price": 7200.00,
                "tags": [1, 2],  # Vegetariano, Sin Gluten
            },
            {
                "name": "Ensalada Vegana Bowl",
                "description": "Quinoa, garbanzos, aguacate, tomates cherry, espinaca y tahini",
                "price": 7900.00,
                "tags": [0, 2, 10],  # Vegano, Sin Gluten, Orgánico
            },
            # Sopas
            {
                "name": "Cazuela de Vacuno",
                "description": "Tradicional sopa chilena con carne de vacuno, zapallo, choclo y papas",
                "price": 8500.00,
                "tags": [],
            },
            {
                "name": "Crema de Zapallo",
                "description": "Suave crema de zapallo con jengibre y crema de leche",
                "price": 5800.00,
                "tags": [1],  # Vegetariano
            },
            # Pastas
            {
                "name": "Fetuccini Alfredo",
                "description": "Pasta fresca con salsa cremosa de parmesano y mantequilla",
                "price": 9800.00,
                "tags": [1],  # Vegetariano
            },
            {
                "name": "Espagueti Boloñesa",
                "description": "Pasta con salsa de carne molida, tomate y hierbas italianas",
                "price": 10500.00,
                "tags": [],
            },
            {
                "name": "Ravioles de Espinaca y Ricotta",
                "description": "Ravioles rellenos de espinaca y ricotta con salsa de tomate albahaca",
                "price": 11200.00,
                "tags": [1],  # Vegetariano
            },
            {
                "name": "Pasta Arrabiata",
                "description": "Penne con salsa de tomate picante, ajo y perejil",
                "price": 9200.00,
                "tags": [1, 0, 4],  # Vegetariano, Vegano, Picante
            },
            # Carnes
            {
                "name": "Bife de Chorizo",
                "description": "Jugoso bife de chorizo de 300g con papas rústicas y vegetales",
                "price": 15900.00,
                "tags": [2],  # Sin Gluten
            },
            {
                "name": "Lomo a la Pimienta",
                "description": "Medallones de lomo con salsa de pimienta verde y puré de papas",
                "price": 17500.00,
                "tags": [],
            },
            {
                "name": "Costillar de Cerdo BBQ",
                "description": "Costillar de cerdo glaseado con salsa BBQ casera y ensalada coleslaw",
                "price": 14800.00,
                "tags": [],
            },
            {
                "name": "Pollo al Limón",
                "description": "Pechuga de pollo con salsa de limón, alcaparras y arroz pilaf",
                "price": 11900.00,
                "tags": [2, 11],  # Sin Gluten, Bajo en Calorías
            },
            # Pescados y Mariscos
            {
                "name": "Salmón a la Plancha",
                "description": "Filete de salmón con espárragos y salsa de eneldo",
                "price": 16500.00,
                "tags": [2, 11],  # Sin Gluten, Bajo en Calorías
            },
            {
                "name": "Paella de Mariscos",
                "description": "Arroz con camarones, calamares, mejillones y azafrán",
                "price": 18900.00,
                "tags": [5, 2],  # Mariscos, Sin Gluten
            },
            {
                "name": "Corvina con Alcaparras",
                "description": "Filete de corvina con salsa de alcaparras, limón y papas al vapor",
                "price": 15200.00,
                "tags": [2],  # Sin Gluten
            },
            # Pizzas
            {
                "name": "Pizza Margherita",
                "description": "Salsa de tomate, mozzarella fresca, albahaca y aceite de oliva",
                "price": 9500.00,
                "tags": [1],  # Vegetariano
            },
            {
                "name": "Pizza Pepperoni",
                "description": "Salsa de tomate, mozzarella y abundante pepperoni",
                "price": 10800.00,
                "tags": [],
            },
            {
                "name": "Pizza Cuatro Quesos",
                "description": "Mozzarella, gorgonzola, parmesano y provolone",
                "price": 11500.00,
                "tags": [1],  # Vegetariano
            },
            {
                "name": "Pizza Vegetariana",
                "description": "Champiñones, pimientos, cebolla, aceitunas y tomate",
                "price": 10200.00,
                "tags": [1],  # Vegetariano
            },
            # Postres
            {
                "name": "Tiramisú",
                "description": "Clásico postre italiano con café, mascarpone y cacao",
                "price": 5500.00,
                "tags": [1, 8],  # Vegetariano, Huevo
            },
            {
                "name": "Cheesecake de Frutos Rojos",
                "description": "Tarta de queso con base de galleta y coulis de frutos rojos",
                "price": 5800.00,
                "tags": [1],  # Vegetariano
            },
            {
                "name": "Brownie con Helado",
                "description": "Brownie de chocolate tibio con helado de vainilla y salsa de chocolate",
                "price": 5200.00,
                "tags": [1, 7],  # Vegetariano, Frutos Secos
            },
            {
                "name": "Flan Casero",
                "description": "Flan tradicional con caramelo casero y crema chantilly",
                "price": 4200.00,
                "tags": [1, 2],  # Vegetariano, Sin Gluten
            },
            # Bebidas
            {
                "name": "Limonada Natural",
                "description": "Limonada fresca con menta y hielo",
                "price": 2500.00,
                "tags": [0, 2],  # Vegano, Sin Gluten
            },
            {
                "name": "Jugo Natural del Día",
                "description": "Jugo de frutas frescas de temporada",
                "price": 2800.00,
                "tags": [0, 2],  # Vegano, Sin Gluten
            },
            {
                "name": "Café Espresso",
                "description": "Café espresso italiano",
                "price": 1800.00,
                "tags": [0],  # Vegano
            },
        ]

        dishes = []

        for dish_data in dishes_data:
            dish = Dish.objects.create(
                name=dish_data["name"],
                description=dish_data["description"],
                price=dish_data["price"],
            )
            # Asignar tags usando los índices
            for tag_index in dish_data.get("tags", []):
                if 0 <= tag_index < len(tags):
                    dish.tags.add(tags[tag_index])
            dishes.append(dish)

        return dishes

    def _create_menus(self, dishes):
        """Crear menús con platos"""
        # Organizar platos por tipo (basado en su índice)
        entradas = dishes[0:4]
        ensaladas = dishes[4:7]
        sopas = dishes[7:9]
        pastas = dishes[9:13]
        carnes = dishes[13:17]
        pescados = dishes[17:20]
        pizzas = dishes[20:24]
        postres = dishes[24:28]
        bebidas = dishes[28:31]

        menus_data = [
            {
                "name": "Menú Ejecutivo",
                "description": "Menú de almuerzo: entrada, plato principal y postre",
                "dishes": [
                    entradas[0],
                    ensaladas[0],
                    carnes[3],
                    postres[3],
                    bebidas[0],
                ],
            },
            {
                "name": "Menú Vegetariano",
                "description": "Selección completa de platos vegetarianos",
                "dishes": [entradas[1], ensaladas[1], pastas[0], pizzas[3], postres[1]],
            },
            {
                "name": "Menú Degustación",
                "description": "Experiencia gastronómica con lo mejor de nuestra cocina",
                "dishes": [
                    entradas[2],
                    ensaladas[2],
                    sopas[0],
                    pescados[0],
                    carnes[0],
                    postres[0],
                ],
            },
            {
                "name": "Menú Italiano",
                "description": "Auténticos sabores de Italia",
                "dishes": [entradas[3], pastas[2], pizzas[0], postres[0], bebidas[2]],
            },
            {
                "name": "Menú del Mar",
                "description": "Los mejores pescados y mariscos",
                "dishes": [
                    entradas[2],
                    ensaladas[1],
                    sopas[1],
                    pescados[1],
                    postres[1],
                ],
            },
        ]

        menus = []
        for menu_data in menus_data:
            menu = Menu.objects.create(
                name=menu_data["name"],
                description=menu_data["description"],
            )
            menu.dishes.set(menu_data["dishes"])
            menus.append(menu)

        return menus

    def _create_tables(self):
        """Crear mesas"""
        tables_data = [
            {"name": "Mesa 1", "capacity": 2},
            {"name": "Mesa 2", "capacity": 2},
            {"name": "Mesa 3", "capacity": 4},
            {"name": "Mesa 4", "capacity": 4},
            {"name": "Mesa 5", "capacity": 4},
            {"name": "Mesa 6", "capacity": 6},
            {"name": "Mesa 7", "capacity": 6},
            {"name": "Mesa 8", "capacity": 8},
            {"name": "Mesa 9", "capacity": 8},
            {"name": "Mesa 10", "capacity": 10},
        ]

        tables = []
        for table_data in tables_data:
            table = Table.objects.create(
                name=table_data["name"],
                capacity=table_data["capacity"],
            )
            tables.append(table)

        return tables

    def _create_reservations(self, tables):
        """Crear reservas de ejemplo"""
        now = timezone.now()
        reservations_data = [
            {
                "table": tables[0],
                "customer_name": "María González",
                "reservation_datetime": now + timedelta(days=1, hours=19),
                "number_of_guests": 2,
            },
            {
                "table": tables[2],
                "customer_name": "Carlos Rodríguez",
                "reservation_datetime": now + timedelta(days=1, hours=20),
                "number_of_guests": 4,
            },
            {
                "table": tables[5],
                "customer_name": "Ana Martínez",
                "reservation_datetime": now + timedelta(days=2, hours=13),
                "number_of_guests": 6,
            },
            {
                "table": tables[7],
                "customer_name": "Juan Pérez",
                "reservation_datetime": now + timedelta(days=2, hours=21),
                "number_of_guests": 8,
            },
            {
                "table": tables[1],
                "customer_name": "Laura Fernández",
                "reservation_datetime": now + timedelta(days=3, hours=19, minutes=30),
                "number_of_guests": 2,
            },
            {
                "table": tables[4],
                "customer_name": "Roberto Sánchez",
                "reservation_datetime": now + timedelta(days=3, hours=20, minutes=30),
                "number_of_guests": 4,
            },
            {
                "table": tables[9],
                "customer_name": "Patricia López",
                "reservation_datetime": now + timedelta(days=4, hours=14),
                "number_of_guests": 10,
            },
        ]

        reservations = []
        for res_data in reservations_data:
            reservation = Reservation.objects.create(**res_data)
            reservations.append(reservation)

        return reservations

    def _create_orders(self, tables, dishes):
        """Crear pedidos de ejemplo"""
        orders_data = [
            {
                "table": tables[0],
                "customer_name": "María González",
                "dishes": [dishes[0], dishes[9], dishes[24], dishes[28]],
                "status": Order.OrderStatus.PENDING,
                "is_paid": False,
            },
            {
                "table": tables[2],
                "customer_name": "Carlos Rodríguez",
                "dishes": [
                    dishes[1],
                    dishes[5],
                    dishes[13],
                    dishes[14],
                    dishes[25],
                    dishes[29],
                ],
                "status": Order.OrderStatus.READY,
                "is_paid": False,
            },
            {
                "table": tables[5],
                "customer_name": "Ana Martínez",
                "dishes": [
                    dishes[2],
                    dishes[4],
                    dishes[17],
                    dishes[18],
                    dishes[19],
                    dishes[26],
                ],
                "status": Order.OrderStatus.DELIVERED,
                "is_paid": True,
            },
            {
                "table": tables[3],
                "customer_name": "Juan Pérez",
                "dishes": [dishes[3], dishes[20], dishes[27], dishes[30]],
                "status": Order.OrderStatus.PENDING,
                "is_paid": False,
            },
            {
                "table": tables[1],
                "customer_name": "Laura Fernández",
                "dishes": [dishes[6], dishes[12], dishes[24], dishes[28]],
                "status": Order.OrderStatus.READY,
                "is_paid": True,
            },
            # Pedido con el mismo cliente en otra mesa (múltiples mesas)
            {
                "table": tables[4],
                "customer_name": "María González",
                "dishes": [dishes[15], dishes[20], dishes[29]],
                "status": Order.OrderStatus.PENDING,
                "is_paid": False,
            },
        ]

        orders = []
        for order_data in orders_data:
            order = Order.objects.create(
                table=order_data["table"],
                customer_name=order_data["customer_name"],
                status=order_data["status"],
                is_paid=order_data["is_paid"],
            )
            order.dishes.set(order_data["dishes"])
            # Calcular y guardar el total
            order.total_amount = order.calculate_total()
            order.save(update_fields=["total_amount"])
            orders.append(order)

        return orders
