import logging
from abc import ABCMeta, abstractmethod
from typing import List

from app.shops.base.advert import Advert


class Driver(metaclass=ABCMeta):
    def __init__(self, request: str, headless: bool = True):
        self.logger = logging.getLogger('driver') #str(self.__class__))
        self.logger.setLevel(logging.INFO)
        self.request = request

    @abstractmethod
    def set_request(self, request: str) -> None:
        pass

    @abstractmethod
    def get_adverts(self) -> List[Advert]:
        pass
