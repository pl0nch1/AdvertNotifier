import asyncio
import platform
from asyncio import Condition, Event
from typing import List

from arsenic import browsers, services, start_session, get_session
from arsenic.constants import SelectorType

from app.shops.avito.advert import AvitoAdvert
from app.shops.base.driver import Driver

OS_DRIVER_MAP = {  # constant file path of Chrome driver
    'Linux': './app/drivers_bin/linux/chromedriver',
    'Windows': './app/drivers_bin/windows/chromedriver.exe',
}


class AvitoDriverAsync(Driver):
    def __init__(self, request: str, headless: bool = True):
        super(AvitoDriverAsync, self).__init__(request, headless)
        self.initialized = Event()
        asyncio.ensure_future(self._init_driver(headless))

    async def _init_driver(self, headless: bool):
        path = OS_DRIVER_MAP.get(platform.system())
        service = services.Chromedriver(binary=path)
        browser = browsers.Chrome(**{"goog:chromeOptions": {
            'args': ['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
        }})

        self.driver = await start_session(service, browser)
        self.initialized.set()

    async def set_request(self, request: str) -> None:
        self.request = request
        await self.driver.get(self.request)

    async def get_adverts(self) -> List[AvitoAdvert]:
        print(f"request is !!!!!!!!!!{self.request}")
        await self.initialized.wait()
        await self.driver.get(self.request)
        # await self.driver.refresh() TODO: refresh doesn't work
        try:
            items = await self.driver.get_elements(0,
                                                   "//h3[contains(@itemprop, 'name') and not(contains(@class, 'title-large'))]",
                                                   selector_type=SelectorType.xpath)

            adverts = []
            for item in items:
                text_coroutine = item.get_text()
                url_coroutine = item.get_element("//./..", selector_type=SelectorType.xpath)
                date_coroutine = item.get_element("//./../../..//div[contains(@class, 'date-text')]",  # TODO find error
                                                  selector_type=SelectorType.xpath)
                price_coroutine = item.get_element("//./../../..//div[contains(@class, 'price')]",
                                                   selector_type=SelectorType.xpath)

                [title, url, time_ago, cost] = await asyncio.gather(text_coroutine, url_coroutine, date_coroutine,
                                                                    price_coroutine)

                adverts.append(AvitoAdvert(title, url, time_ago, cost))

            return adverts

        except Exception:
            self.logger.error('No such element')
            return []
