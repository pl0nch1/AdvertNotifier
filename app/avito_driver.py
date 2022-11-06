import asyncio
import platform
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver
from app.telegram.teelgram_staff import get_client, send_adverts, start_telegram, Advert
from utils import LOGGER
from yaml import dump, load, Dumper, Loader

OS_DRIVER_MAP = {  # constant file path of Chrome driver
    'Linux': './app/drivers/linux/chromedriver',
    'Windows': './app/drivers//windows/chromedriver.exe',
}


class AvitoDriver:
    def __init__(self, request: str):
        self.request = request
        self.init_driver()

    def init_driver(self):
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
        options.add_argument("--headless")
        if platform.system() == 'Linux':
            options.add_argument("--disable-dev-shm-usage")
        self.driver: WebDriver = webdriver.Chrome(options=options, service=path)
        self.driver.maximize_window()
        self.driver.get(
            self.request)

    def set_request(self, request: str):
        self.request = request
        self.driver.get(self.request)

    def get_adverts(self):
        self.driver.refresh()
        try:
            items = self.driver.find_elements(By.XPATH,
                                              "//h3[contains(@itemprop, 'name') and not(contains(@class, 'title-large'))]")
            adverts = [Advert(item.text,
                              item.find_element(By.XPATH, "./..").get_attribute('href'),
                              item.find_element(By.XPATH, "./../../..").find_element(By.XPATH,
                                                                                     ".//div[contains(@class, 'date-text')]").text,
                              item.find_element(By.XPATH, "./../../..").find_element(By.XPATH,
                                                                                     ".//div[contains(@class, 'price')]").text)
                       for item in items]
            return adverts
        except NoSuchElementException:
            LOGGER.error('No such element')
            return []

    def close(self):
        self.driver.close()
