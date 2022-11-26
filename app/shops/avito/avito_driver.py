import platform
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver

from app.shops.avito.advert import AvitoAdvert
from app.shops.base.driver import Driver

OS_DRIVER_MAP = {  # constant file path of Chrome driver
    'Linux': './app/drivers_bin/linux/chromedriver',
    'Windows': './app/drivers_bin/windows/chromedriver.exe',
}


class AvitoDriver(Driver):
    def __init__(self, request: str, headless: bool = True):
        super(AvitoDriver, self).__init__(request, headless)
        self._init_driver(headless)

    def _init_driver(self, headless: bool):
        path = Service(OS_DRIVER_MAP.get(platform.system()))
        options = webdriver.ChromeOptions()  # Initializing Chrome Options from the Webdriver
        options.add_experimental_option("useAutomationExtension",
                                             False)  # Adding Argument to Not Use Automation Extension
        options.add_experimental_option("excludeSwitches",
                                             ["enable-automation"])  # Excluding enable-automation Switch
        options.add_argument("disable-popup-blocking")
        options.add_argument("disable-notifications")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        if headless:
            options.add_argument("--headless")
        if platform.system() == 'Linux':
            options.add_argument("--disable-dev-shm-usage")
        self.driver: WebDriver = webdriver.Chrome(options=options, service=path)
        self.driver.maximize_window()
        self.driver.get(
            self.request)

    def set_request(self, request: str) -> None:
        self.request = request
        self.driver.get(self.request)

    def get_adverts(self) -> List[AvitoAdvert]:
        self.driver.refresh()
        try:
            items = self.driver.find_elements(By.XPATH,
                                              "//h3[contains(@itemprop, 'name') and not(contains(@class, 'title-large'))]")
            adverts = [AvitoAdvert(item.text,
                                   item.find_element(By.XPATH, "./..").get_attribute('href'),
                                   item.find_element(By.XPATH, "./../../..").find_element(By.XPATH,
                                                                                     ".//div[contains(@class, 'date-text')]").text,
                                   item.find_element(By.XPATH, "./../../..").find_element(By.XPATH,
                                                                                     ".//div[contains(@class, 'price')]").text)
                       for item in items]
            return adverts
        except NoSuchElementException:
            self.logger.error('No such element')
            return []
