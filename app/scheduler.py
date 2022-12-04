import asyncio
import logging

from app.shops.avito.avito_driver_manager import AvitoDriverManager
from app.telegram.telegram_facade import TelegramFacade
from app.user_management.user_manager import UserManager
from app.context import user_manager

logger = logging.getLogger('scheduler')
logger.setLevel(logging.INFO)


class Scheduler:
    def __init__(self):
        self.user_manager = user_manager
        # self.user_manager.subscribe('tech9998', 10)
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx_2060')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=fatshark')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=skyzone')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=dji_fpv')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=vista')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx_4060')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx')
        # self.user_manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx')
        self.avito = AvitoDriverManager(self.user_manager, headless=False)
        self.avito.load_drivers()
        self.telegram = TelegramFacade.with_default_client()

    def schedule(self):
        async def a_schedule():
            while True:
                fetch_result = await self.avito.execute_drivers()
                try:
                    for tg_id, requests in self.user_manager.request_items():
                        print(requests)
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
