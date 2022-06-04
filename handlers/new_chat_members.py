from loader import dp, bot
from aiogram import types
from core.tools import MessageBox


@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message: types.Message):
    new_user = message.new_chat_members[0]
    user_name = None
    if new_user.first_name:
        user_name = new_user.first_name
    elif new_user.username:
        user_name = new_user.username

    bot_obj = await bot.me

    bot_username = bot_obj['username']

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button = types.InlineKeyboardButton("Нажми на меня, чтобы узнать информацию!",
                                        callback_data='get_info',
                                        url=f'https://t.me/{bot_username}/')

    keyboard.add(button)

    msg = await bot.send_message(message.chat.id,
                                 f"Добро пожаловать, {user_name}!" if bot_username else "Добро пожаловать!",
                                 reply_markup=keyboard)

    MessageBox.set_chat_id(message.chat.id)
    MessageBox.put(msg, new_user.id)
