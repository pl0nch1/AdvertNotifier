from abc import abstractmethod, ABCMeta
from typing import List, Dict

from app.shops.base.advert import Advert
from app.user_management.user_manager import UserManager


class DriverManager(metaclass=ABCMeta):
    def __init__(self, user_manager: UserManager, headless: bool):
        pass

    @abstractmethod
    def load_drivers(self) -> None:
        pass

    @abstractmethod
    def execute_drivers(self) -> Dict[str, List[Advert]]:
        pass


