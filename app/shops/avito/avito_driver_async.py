import asyncio
import platform
from asyncio import Event
from typing import List

from arsenic import browsers, services, start_session
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
        await self.initialized.wait()
        await self.driver.get(self.request)
        try:
            print("123")
            items = await self.driver.get_elements("//h3[contains(@itemprop, 'name') and not(contains(@class, 'title-large'))]",
                                                   selector_type=SelectorType.xpath)
            print("147981895418947618947" + str(items))
            adverts = []
            for item in items:
                text_coroutine = item.get_text()
                url_coroutine = item.get_element("./../../a", selector_type=SelectorType.xpath)
                date_coroutine = item.get_element("./../../..//div[contains(@data-marker, 'item-date')]",  # TODO find error
                                                  selector_type=SelectorType.xpath)
                price_coroutine = item.get_element("./../../..//span[contains(@data-marker, 'item-price')]/span",
                                                   selector_type=SelectorType.xpath)

                [title, url, time_ago, cost] = await asyncio.gather(text_coroutine, url_coroutine, date_coroutine,
                                                                    price_coroutine)

                adverts.append(AvitoAdvert(title,
                                           await url.get_property("href"),
                                           await time_ago.get_text(),
                                           await cost.get_text()))

            return list(reversed(adverts))

        except Exception as e:
            self.logger.error(f'Failed to parse adverts: {e}')
            return []
