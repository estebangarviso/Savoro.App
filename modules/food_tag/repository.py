"""
FoodTag repository
"""
from core import BaseRepository, Injectable
from .models import FoodTag


@Injectable()
class FoodTagRepository(BaseRepository[FoodTag]):
    """Repository for FoodTag entity"""

    def __init__(self):
        super().__init__(FoodTag)
