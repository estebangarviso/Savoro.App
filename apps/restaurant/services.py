"""
Servicios para la gestión de filtros de platos y categorías
Aplicando el principio de Responsabilidad Única (Single Responsibility Principle)
"""

from django.db import models
from django.db.models import Count, Q, QuerySet
from django.http import HttpRequest
from typing import Optional, Dict, Any
from .models import Dish, Category, FoodTag


# ============================================================================
# SERVICIOS PARA PLATOS
# ============================================================================


class DishFilterService:
    """
    Servicio responsable de aplicar filtros a los querysets de platos
    Responsabilidad única: Filtrado de platos
    """

    @staticmethod
    def apply_filters(
        queryset: QuerySet[Dish],
        search_query: Optional[str] = None,
        category_id: Optional[str] = None,
        tag_id: Optional[str] = None,
    ) -> QuerySet[Dish]:
        """
        Aplica múltiples filtros a un queryset de platos

        Args:
            queryset: QuerySet base de platos
            search_query: Texto para buscar en nombre y descripción
            category_id: ID de la categoría a filtrar
            tag_id: ID del tag a filtrar

        Returns:
            QuerySet filtrado
        """
        if search_query:
            queryset = DishFilterService._apply_search_filter(queryset, search_query)

        if category_id:
            queryset = DishFilterService._apply_category_filter(queryset, category_id)

        if tag_id:
            queryset = DishFilterService._apply_tag_filter(queryset, tag_id)

        return queryset

    @staticmethod
    def _apply_search_filter(
        queryset: QuerySet[Dish], search_query: str
    ) -> QuerySet[Dish]:
        """Aplica filtro de búsqueda por texto"""
        return queryset.filter(
            models.Q(name__icontains=search_query)
            | models.Q(description__icontains=search_query)
        )

    @staticmethod
    def _apply_category_filter(
        queryset: QuerySet[Dish], category_id: str
    ) -> QuerySet[Dish]:
        """Aplica filtro por categoría"""
        return queryset.filter(category_id=category_id)

    @staticmethod
    def _apply_tag_filter(queryset: QuerySet[Dish], tag_id: str) -> QuerySet[Dish]:
        """Aplica filtro por tag (con distinct para evitar duplicados)"""
        return queryset.filter(tags__id=tag_id).distinct()


class DishQueryService:
    """
    Servicio responsable de construir queries optimizadas de platos
    Responsabilidad única: Construcción de queries
    """

    @staticmethod
    def get_base_queryset() -> QuerySet[Dish]:
        """Obtiene el queryset base de platos activos con relaciones precargadas"""
        return Dish.objects.filter(deleted=False).prefetch_related("tags", "category")

    @staticmethod
    def get_filtered_dishes(
        search_query: Optional[str] = None,
        category_id: Optional[str] = None,
        tag_id: Optional[str] = None,
    ) -> QuerySet[Dish]:
        """
        Obtiene platos filtrados con relaciones optimizadas

        Returns:
            QuerySet de platos filtrados
        """
        queryset = DishQueryService.get_base_queryset()
        return DishFilterService.apply_filters(
            queryset, search_query, category_id, tag_id
        )


class CategoryQueryService:
    """
    Servicio responsable de construir queries de categorías con platos
    Responsabilidad única: Queries de categorías
    """

    @staticmethod
    def get_categories_with_dishes(
        dishes_queryset: QuerySet[Dish],
    ) -> QuerySet[Category]:
        """
        Obtiene categorías con sus platos filtrados

        Args:
            dishes_queryset: QuerySet de platos a incluir

        Returns:
            QuerySet de categorías con platos precargados
        """
        return (
            Category.objects.filter(deleted=False)
            .prefetch_related(
                models.Prefetch(
                    "dishes",
                    queryset=dishes_queryset,
                )
            )
            .order_by("name")
        )


class FilterContextBuilder:
    """
    Servicio responsable de construir el contexto para las vistas con filtros
    Responsabilidad única: Construcción del contexto de vistas
    """

    @staticmethod
    def build_filter_context(request: HttpRequest) -> Dict[str, Any]:
        """
        Construye el contexto completo para la vista de índice con filtros

        Args:
            request: HttpRequest con los parámetros de filtro

        Returns:
            Diccionario con el contexto para el template
        """
        # Extraer parámetros de filtro
        search_query = request.GET.get("search", "")
        category_filter = request.GET.get("category", "")
        tag_filter = request.GET.get("tag", "")

        # Obtener platos filtrados
        filtered_dishes = DishQueryService.get_filtered_dishes(
            search_query=search_query, category_id=category_filter, tag_id=tag_filter
        )

        # Obtener categorías con platos filtrados
        categories = CategoryQueryService.get_categories_with_dishes(filtered_dishes)

        # Obtener platos sin categoría
        uncategorized_dishes = filtered_dishes.filter(category__isnull=True)

        # Obtener datos para los selectores de filtros
        all_categories = Category.objects.filter(deleted=False).order_by("name")
        all_tags = FoodTag.objects.all().order_by("name")

        return {
            "categories": categories,
            "uncategorized_dishes": uncategorized_dishes,
            "all_categories": all_categories,
            "all_tags": all_tags,
            "search_query": search_query,
            "category_filter": category_filter,
            "tag_filter": tag_filter,
        }


# ============================================================================
# SERVICIOS PARA CATEGORÍAS
# ============================================================================


class CategoryFilterService:
    """
    Servicio responsable de aplicar filtros a los querysets de categorías
    Responsabilidad única: Filtrado de categorías
    """

    @staticmethod
    def apply_filters(
        queryset: models.QuerySet[Category],
        search_query: Optional[str] = None,
    ) -> models.QuerySet[Category]:
        """
        Aplica filtros a un queryset de categorías

        Args:
            queryset: QuerySet base de categorías
            search_query: Texto para buscar en nombre

        Returns:
            QuerySet filtrado
        """
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset


class CategoryStatsService:
    """
    Servicio responsable de obtener estadísticas de categorías
    Responsabilidad única: Cálculo de estadísticas
    """

    @staticmethod
    def get_categories_with_dish_count() -> models.QuerySet[Category]:
        """
        Obtiene categorías con el conteo de platos asociados

        Returns:
            QuerySet de categorías con anotación de conteo de platos
        """
        return (
            Category.objects.filter(deleted=False)
            .annotate(dish_count=Count("dishes", filter=Q(dishes__deleted=False)))
            .order_by("-dish_count", "name")
        )

    @staticmethod
    def get_filtered_categories_with_stats(
        search_query: Optional[str] = None,
    ) -> models.QuerySet[Category]:
        """
        Obtiene categorías filtradas con estadísticas

        Args:
            search_query: Texto para buscar

        Returns:
            QuerySet de categorías filtradas con stats
        """
        queryset = CategoryStatsService.get_categories_with_dish_count()
        return CategoryFilterService.apply_filters(queryset, search_query)


class CategoryContextBuilder:
    """
    Servicio responsable de construir el contexto para las vistas de categorías
    Responsabilidad única: Construcción del contexto de vistas
    """

    @staticmethod
    def build_list_context(request: HttpRequest) -> Dict[str, Any]:
        """
        Construye el contexto completo para la vista de listado de categorías

        Args:
            request: HttpRequest con los parámetros de filtro

        Returns:
            Diccionario con el contexto para el template
        """
        # Extraer parámetros de filtro
        search_query = request.GET.get("search", "")

        # Obtener categorías filtradas con estadísticas
        categories = CategoryStatsService.get_filtered_categories_with_stats(
            search_query
        )

        return {
            "categories": categories,
            "search_query": search_query,
            "total_count": categories.count(),
        }
