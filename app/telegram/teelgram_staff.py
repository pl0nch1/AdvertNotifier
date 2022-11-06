import asyncio
import sys
from dataclasses import dataclass
from typing import List
from hashlib import md5
from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.\
api_id = 22659155
api_hash = 'dac484ee681fd92f2e6a8da13e561b52'

NOTIFICANTS = ['qu1ckly',
               'pl0nch1']


@dataclass
class Advert:
    title: str
    url: str
    time_ago: str
    cost: str

    def __str__(self):
        return f'{url(self.title, self.url)} ({self.cost}) - {self.time_ago}'

    def __hash__(self):
        return int.from_bytes(md5(bytes(self.url, 'UTF-8')).digest(), sys.byteorder)


def url(text, link):
    return f'[{text}]({link})'


async def send_adverts(tg_client: TelegramClient, adverts: List[Advert]):
    for i in range(0, len(adverts), 15):
        for notificant in NOTIFICANTS:
            await tg_client.send_message(notificant, '\n'.join(map(str, adverts[i:i+15])), link_preview=False)


def get_client():
    return TelegramClient('session_name', api_id, api_hash)


def start_telegram(client):
    @client.on(events.NewMessage(pattern='(?i)hi|hello'))
    async def handler(event):
        await event.respond(str((await event.get_sender()).username))
    client.run_until_disconnected()
