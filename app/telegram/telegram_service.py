import asyncio
import logging

from telethon import events, TelegramClient, types, Button
from telethon.events import NewMessage
from telethon.events.common import EventBuilder
from telethon.tl.types import KeyboardButton

from app.context import user_manager, is_admin
from app.errors import OutOfQuotaException, UserUnsubscribed, UserHasNoRequests

logger = logging.getLogger('messages_handler')
logger.setLevel(logging.INFO)


async def handle_subscribe(client: TelegramClient, event, arg):
    sender = await event.get_sender()
    async with client.conversation(await event.get_sender()) as conv:
        if not arg:
            buttons = client.build_reply_markup([
                Button.inline('+1 запрос к квоте', 1),
                Button.inline('+3 запроса к квоте', 3)
            ])
            message = await client.send_message(sender, 'Оформить подписку можно в любое время с помощью онлайн кассы',
                                                buttons=buttons)
            arg = int((await conv.wait_event(events.CallbackQuery(sender.username))).data)
            await client.delete_messages(sender, [message.id])
        await client.send_message(sender, f'Оформляем подписку на {arg} запроса(-ов)...')
        user_manager.subscribe(sender.username, arg)

async def show_help(client, user_id):
    text = '\n'.join(handlers.keys())
    await client.send_message(user_id, text)


def start_telegram(client: TelegramClient):
    with client:
        @client.on(events.NewMessage())
        async def handle(event):
            text = event.message.message.strip()
            logger.info(f'Got {text} from {await event.get_sender()}')
            if ' ' not in text:
                command = text
                arg = None
            else:
                space_index = text.index(' ')
                command = text[:space_index:]
                arg = text[space_index+1::]
            handler = handlers.get(command)
            if not handler:
                await event.respond('Команда не распознана')
                await show_help(client, (await event.get_sender()).id)
            else:
                await handler(client, event, arg)
        client.run_until_disconnected()


handlers = {
    '/subscribe': handle_subscribe
}