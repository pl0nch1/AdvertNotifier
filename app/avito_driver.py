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

PATH = Service(OS_DRIVER_MAP.get(platform.system()))
MEMORY_PATH = 'listed.yaml'
options = webdriver.ChromeOptions()  # Initializing Chrome Options from the Webdriver
options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
options.add_argument("disable-popup-blocking")
options.add_argument("disable-notifications")
options.add_argument("--disable-gpu")  ##renderer timeout
options.add_argument("--no-sandbox")
options.add_argument("--headless")

if platform.system() == 'Linux':
    options.add_argument("--disable-dev-shm-usage")


# item: WebElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, f"//h3[contains(@itemprop, 'name')]")))
# item.click()


try:
    with open(MEMORY_PATH, 'r') as file:
        memory = load(file, Loader=Loader)
except FileNotFoundError:
    memory = set()
    with open(MEMORY_PATH, 'w') as file:
        dump(memory, file, Dumper=Dumper)

driver: WebDriver = webdriver.Chrome(options=options, service=PATH)
driver.maximize_window()
driver.get('https://www.avito.ru/sankt-peterburg/tovary_dlya_kompyutera/komplektuyuschie/videokarty?cd=1&localPriority=1&s=104')


async def do(client):
    driver.refresh()
    try:
        items = driver.find_elements(By.XPATH,
                                     "//h3[contains(@itemprop, 'name') and not(contains(@class, 'title-large'))]")
        adverts = [Advert(item.text,
                          item.find_element(By.XPATH, "./..").get_attribute('href'),
                          item.find_element(By.XPATH, "./../../..").find_element(By.XPATH,
                                                                                 ".//div[contains(@class, 'date-text')]").text,
                          item.find_element(By.XPATH, "./../../..").find_element(By.XPATH,
                                                                                 ".//span[contains(@class, 'price-text')]").text
                          )
                   for item in items]
        filtered_adverts = list(filter(lambda advert: hash(advert) not in memory, adverts))
        filtered_adverts.reverse()
        memory.update(set({hash(advert) for advert in filtered_adverts}))
        if filtered_adverts:
            await send_adverts(client, filtered_adverts)
    except Exception as e:
        LOGGER.exception('Failed to get new adverts', exc_info=e)

    with open(MEMORY_PATH, 'w') as file:
        dump(memory, file, Dumper=Dumper, allow_unicode=True)
    await asyncio.sleep(random.uniform(8.0, 12.0))


async def start_browser(client):
    while True:
        try:
            await do(client)
        except NoSuchWindowException as e:
            raise
        except Exception as e:
            LOGGER.exception('Exception occured:', e)


with get_client() as client:
    loop = asyncio.get_event_loop()
    loop.create_task(start_browser(client))
    start_telegram(client)
