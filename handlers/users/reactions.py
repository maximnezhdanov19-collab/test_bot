from aiogram import F, types
from data.setting import bot
from handlers.users import router
from middlewares.all_in_one import count_users_message_plus_one

@router.message_reaction()
async def handle_reaction(reaction: types.MessageReactionUpdated):
    new_reaction = reaction.new_reaction[0].emoji
    print(new_reaction)
    if new_reaction == '❤':
        count_users_message_plus_one(reaction.chat.id)
        await bot.send_message(chat_id=reaction.chat.id, text='Спасибо за любовь! 💖')
    elif new_reaction == '👎':
        count_users_message_plus_one(reaction.chat.id)
        await bot.send_message(chat_id=reaction.chat.id, text='Жаль, что не понравилось... 😢')
