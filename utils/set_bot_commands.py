from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начать работу'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='game_clubs', description='Посмотреть игровые клубы'),
        BotCommand(command='make_order', description='Сделать заказ'),
        BotCommand(command='admin_cmd', description='Запросить права админа'),
        BotCommand(command='add_admin', description='Сделать админом'),
        BotCommand(command='quiz', description='Викторина'),
        BotCommand(command='hacking', description='Взлом'),
        BotCommand(command='advertisement', description='Отправить рекламу'),
        BotCommand(command='ref_link', description='Пригласить')
    ]

    await bot.set_my_commands(commands=commands)
