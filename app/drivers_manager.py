from typing import Dict
from avito_driver import AvitoDriver

class DriversManager:
    def __init__(self):
        self.drivers: Dict[str, AvitoDriver] = {}

