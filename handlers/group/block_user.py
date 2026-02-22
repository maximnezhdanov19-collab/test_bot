# import datetime
#
# from aiogram import types
# from aiogram.filters import Command
# from aiogram.types.chat_permissions import ChatPermissions
#
# from data.setting import bot
# from handlers.group import router
#
#
# @router.message(Command('block'))
# async def block(message: types.Message):
#     user = message.from_user
#
#     date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
#     permissions = ChatPermissions(can_send_messages=False)
#
#     try:
#         await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user.id, permissions=permissions,
#                                        until_date=date)
#     except Exception as e:
#         print(e)
#
#
# @router.message(Command('unban'))
# async def unblock(message: types.Message):
#     try:
#         await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
#     except:
#         print('ERROR')
