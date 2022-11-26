from typing import List

from telethon import TelegramClient

from app.shops.base.advert import Advert
from app.telegram.telegram_notifier import TelegramNotifier
from app.telegram.telegram_service import start_telegram
from app.telegram.telegram_configs import api_id, api_hash


class TelegramFacade:
    def __init__(self, client: TelegramClient, notifier: TelegramNotifier = None):
        self.client = client
        self.notifier = TelegramNotifier(self.client) if notifier is None else notifier

    @classmethod
    def with_default_client(cls):
        return cls(TelegramClient('session_name', api_id, api_hash))

    def start_telegram(self):
        start_telegram(self.client)

    async def send_adverts(self, destination: str, adverts: List[Advert]):
        await self.notifier.send_adverts(destination, adverts)