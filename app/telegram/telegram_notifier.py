from typing import List
from telethon import TelegramClient

from app.shops.base.advert import Advert


class TelegramNotifier:
    def __init__(self, tg_client: TelegramClient):
        self.client = tg_client

    async def send_adverts(self, destination: str, adverts: List[Advert]):
        for i in range(0, len(adverts), 15):
            await self.client.send_message(destination, '\n'.join(map(str, adverts[i:i+15])), link_preview=False)


