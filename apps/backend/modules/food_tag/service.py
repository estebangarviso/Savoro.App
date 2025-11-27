"""
FoodTag service
"""
from core import BaseService, Injectable
from .repository import FoodTagRepository


@Injectable()
class FoodTagService(BaseService):
    """Service for FoodTag business logic"""

    def __init__(self):
        self.repository = FoodTagRepository()
