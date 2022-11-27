import logging
from typing import Dict, List

from app.shops.avito.advert import AvitoAdvert
from app.shops.avito.avito_driver_async import AvitoDriverAsync
from app.shops.base.driver_manager import DriverManager
from app.user_management.user_manager import UserManager

logger = logging.getLogger('app.drivers_manager')
logger.setLevel(logging.INFO)


class AvitoDriverManager(DriverManager):
    def __init__(self, user_manager: UserManager, headless=True):
        super().__init__(user_manager, headless)
        self.headless = headless
        self.drivers: Dict[str, AvitoDriverAsync] = {}
        self.user_manager = user_manager

    def load_drivers(self) -> None:
        logger.info('starting drivers')
        failed = False
        for tg_id, requests in self.user_manager.request_items():
            for request in requests:
                try:
                    if self.drivers.get(request):
                        continue
                    self.drivers[request] = AvitoDriverAsync(request, self.headless)
                except Exception as e:
                    failed = True
                    logger.error(f'Failed to initialize driver on {request} with tg_id={tg_id}', exc_info=e)
        if failed:
            raise RuntimeError('Application failed to start: see errors above')

    async def execute_drivers(self) -> Dict[str, List[AvitoAdvert]]:
        return {request: await driver.get_adverts() for request, driver in self.drivers.items()}
