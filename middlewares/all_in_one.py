from aiogram import BaseMiddleware
from aiogram import types
from time import time

blocked_users_fast_messages = []
updates = {}
unlocked_time = {}
premium_users = []
counts_users_messages = {}
admins = []

SLEEP_TIME = 5

def get_admin_user_list():
    return admins

def get_premium_user_list():
    return premium_users

def give_premium(id):
    if id not in premium_users:
        premium_users.append(id)

def admin(id):
    if id not in admins:
        admins.append(id)

def count_users_message_plus_one(id):
    counts_users_messages[id] += 1

def checking(id):

    if id not in unlocked_time:
        unlocked_time.update({id: time()})

    user_updates = updates[id][-4:]
    if len(user_updates) > 3:

        update_time_list = []
        for i in range(len(user_updates)):
            print('Итерация')
            update_time = user_updates[i]
            update_time_list.append(update_time)

        difference = update_time_list[-1] - update_time_list[0]
        print(difference)

        if difference < 10:
            blocked_users_fast_messages.append(id)
            if time() > unlocked_time[id]:
                print(time(), unlocked_time[id])
                unlocked_time[id] = time() + SLEEP_TIME

def checking_messages(id):

    if id not in counts_users_messages:
        counts_users_messages.update({id: 0})

    if counts_users_messages[id] > 5 and id not in premium_users:
        return False
    else:
        return True


class AllInOne(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict) -> None:

        if update.message_reaction != None:
            return

        id = update.message.chat.id

        if id in updates:
            updates[id].append(time())
        else:
            updates.update({id:[time()]})

        if id not in blocked_users_fast_messages:
            checking(id)

        if unlocked_time[id] <= time() and id in blocked_users_fast_messages:
            updates[id] = []
            blocked_users_fast_messages.remove(id)

        if id not in blocked_users_fast_messages:
            print('on_pre_process_update')
        else:
            await update.message.answer(text='<b>Вы заблокированы (Спам)!</b> Попробуйте позже', parse_mode='HTML')

    async def on_post_process_update(self, update: types.Update, data: dict) -> None:

        id = update.message.from_user.id
        if id not in blocked_users_fast_messages:
            print('on_post_process_update')

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:

        id = message.from_user.id
        if id not in blocked_users_fast_messages:
            print('on_pre_process_message')

    async def on_post_process_message(self, update: types.Message, data: dict) -> None:

        id = update.from_user.id
        if id not in blocked_users_fast_messages:
            print('on_post_process_message')

    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, data: dict) -> None:

        id = callback.message.from_user.id
        if id not in blocked_users_fast_messages:
            print('on_pre_process_callback_query')

    async def on_post_process_callback_query(self, update: types.CallbackQuery, data: dict) -> None:

        id = update.message.from_user.id
        if id not in blocked_users_fast_messages:
            print('on_post_process_callback_query')

    async def __call__(self, handler, event: types.Update, data: dict):
        await self.on_pre_process_update(event, data)

        if isinstance(event.message, types.Message):

            await self.on_pre_process_message(event.message, data)
        elif isinstance(event.callback_query, types.CallbackQuery):

            await self.on_pre_process_callback_query(event.callback_query, data)
        else:
            print('Неизвестно')

        if event.message_reaction != None:
            await handler(event, data)
            return

        responce = 0
        id = event.message.from_user.id

        if id not in blocked_users_fast_messages:
            responce = await handler(event, data)

        if isinstance(event.message, types.Message):

            await self.on_post_process_message(event.message, data)
        elif isinstance(event.callback_query, types.CallbackQuery):

            await self.on_post_process_callback_query(event.callback_query, data)
        else:
            print('Неизвестно')

        await self.on_post_process_update(event, data)

        if id not in blocked_users_fast_messages:
            return responce
