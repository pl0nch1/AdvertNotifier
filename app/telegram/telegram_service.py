import asyncio

from telethon import events, TelegramClient
from app.context import user_manager, is_admin
from app.errors import OutOfQuotaException, UserUnsubscribed, UserHasNoRequests


def start_telegram(client: TelegramClient):
    with client:
        @client.on(events.NewMessage(pattern='(?i)hi|hello'))
        async def handler(event):
            await event.respond(str((await event.get_sender()).username))

        @client.on(events.NewMessage(pattern='(?i)/subscribe .+'))
        async def subscribe_handler(event):
            sender_id = (await event.get_sender()).username
            if not is_admin(sender_id):  # TODO: add admin check decorator
                await event.respond('You are not admin')
                return
            tg_id = event.raw_text.split(' ')[1]
            n_requests = int(event.raw_text.split(' ')[2])
            user_manager.subscribe(tg_id, n_requests)
            await event.respond(f'Subscribed {tg_id} for {n_requests} requests')

        @client.on(events.NewMessage(pattern='(?i)/add .+'))
        async def add_request_handler(event):
            sender_id = (await event.get_sender()).username
            req = event.raw_text.split(' ')[1]

            try:
                user_manager.append_request(sender_id, req)
                await event.respond('Запрос добавлен')
            except OutOfQuotaException as e:
                await event.respond("У вас закончились запросы")
            except UserUnsubscribed as e:
                await event.respond("У вас закончилась подписка")

        @client.on(events.NewMessage(pattern='(?i)/remove .+'))
        async def remove_request_handler(event):
            sender_id = (await event.get_sender()).username
            ind = int(event.raw_text.split(' ')[1]) - 1
            if isinstance(ind, int):
                user_manager.release_request(sender_id, ind)
                await event.respond('Запрос удален')
            else:
                await event.respond('Неверный номер запроса')

        @client.on(events.NewMessage(pattern='(?i)/list'))
        async def list_requests_handler(event):
            sender_id = (await event.get_sender()).username

            res = ''
            try:
                for ind, req in enumerate(user_manager.list_requests(sender_id)):
                    res += f'{ind + 1}: {req}\n'
                await event.respond(res, link_preview=False)

            except UserHasNoRequests as e:
                await event.respond('У вас нет запросов')

        client.run_until_disconnected()
