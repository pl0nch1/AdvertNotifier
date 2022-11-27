import asyncio

from telethon import events, TelegramClient


def start_telegram(client: TelegramClient):
    with client:
        @client.on(events.NewMessage(pattern='(?i)hi|hello'))
        async def handler(event):
            await event.respond(str((await event.get_sender()).username))
        # client.run_until_disconnected()
        asyncio.get_event_loop().run_forever()