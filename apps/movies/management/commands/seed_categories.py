from django.core.management.base import BaseCommand
from apps.movies.models import Categories


class Command(BaseCommand):
    help = "Seed the database with initial movie categories"

    def handle(self, *args, **options):
        categories_data = [
            {"name": "Acción", "minimum_age": 13},
            {"name": "Aventura", "minimum_age": 10},
            {"name": "Comedia", "minimum_age": 0},
            {"name": "Drama", "minimum_age": 13},
            {"name": "Terror", "minimum_age": 16},
            {"name": "Ciencia Ficción", "minimum_age": 13},
            {"name": "Romance", "minimum_age": 13},
            {"name": "Thriller", "minimum_age": 16},
            {"name": "Animación", "minimum_age": 0},
            {"name": "Documental", "minimum_age": 0},
            {"name": "Fantasía", "minimum_age": 10},
            {"name": "Misterio", "minimum_age": 13},
            {"name": "Musical", "minimum_age": 0},
            {"name": "Western", "minimum_age": 13},
            {"name": "Biografía", "minimum_age": 10},
        ]

        created_count = 0
        for category_data in categories_data:
            category, created = Categories.objects.get_or_create(
                name=category_data["name"],
                defaults={"minimum_age": category_data["minimum_age"]},
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Category already exists: {category.name}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} new categories")
        )
