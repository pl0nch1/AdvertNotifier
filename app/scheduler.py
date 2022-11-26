import asyncio
import logging

from app.shops.avito.avito_driver_manager import AvitoDriverManager
from app.telegram.telegram_facade import TelegramFacade
from app.user_management.user_manager import UserManager

logger = logging.getLogger('scheduler')
logger.setLevel(logging.INFO)


class Scheduler:
    def __init__(self):
        self.user_manager = UserManager()
        self.user_manager.load()
        self.avito = AvitoDriverManager(self.user_manager)
        self.avito.load_drivers()
        self.telegram = TelegramFacade.with_default_client()

    def schedule(self):
        async def a_schedule():
            while True:
                fetch_result = self.avito.execute_drivers()
                try:
                    for tg_id, requests in self.user_manager.request_items():
                        sent_result = await asyncio.gather(*[self.telegram.send_adverts(tg_id, fetch_result[request])
                                                             for request
                                                             in requests])
                except Exception as e:
                    logger.error(e)
                await asyncio.sleep(5)
        asyncio.ensure_future(a_schedule())
        self.telegram.start_telegram()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.schedule()
