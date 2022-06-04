import loguru
from aiogram.types import InputFile

from loader import dp, bot
from aiogram import types
from core.tools import MessageBox

from aiogram.utils.emoji import emojize

PICTURE_ID = None
VIDEO_ID_1 = None
VIDEO_ID_2 = None


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    if message.chat.id < 0:
        return

    global PICTURE_ID, VIDEO_ID_1, VIDEO_ID_2

    picture_path = "media/pics/NFT-fl.jpg"
    if not PICTURE_ID:
        msg = await bot.send_photo(message.chat.id, InputFile(picture_path))
        PICTURE_ID = msg.photo[-1].file_id
    else:
        await bot.send_photo(message.chat.id, PICTURE_ID)

    info_message_1_1 = """
:diamond_shape_with_a_dot_inside: Рады видеть вас в нашей группе!\n
Fluor Space NFT - Это NFT пространство в реальном мире на базе лофт помещения премиум класса и с собственной \
    производственной базой по изготовлению флуоресцентного декора, одежды и аксессуаров, что позволяет осуществлять \
    продажу реальных товаров через продажу NFT, как это делают сейчас ведущие бренды. В планы сообщества входят: \
    совместные спейсы, shill-чаты, проведение коллабораций и взаимный пиар.\n
Наша задача сейчас - сделать мощное сообщество, которое будет помогать продвигаться NFT-художникам, а так же \
    взаимный пиар. Степень вашего развития с нами зависит только от погруженности в проект. Самое главное здесь \
    как в любом комьюнити - синергия.\n
:diamond_shape_with_a_dot_inside: Сайт проекта, где можно познакомиться с производственными возможностями \
    и получить информацию о сообществе - https://fluor.space/\n"""

    await bot.send_message(message.chat.id, emojize(info_message_1_1))

    video_path_1 = "media/vids/fluor_space_pr.mp4"
    if not VIDEO_ID_1:
        msg = await bot.send_video(message.chat.id, InputFile(video_path_1))
        VIDEO_ID_1 = msg.video.file_id
    else:
        await bot.send_video(message.chat.id, VIDEO_ID_1)

    info_message_1_2 = """
:diamond_shape_with_a_dot_inside:Постоянное выставочное пространство, аудитории для встреч, лекций и \
    коллабораций находится рядом с Метро Бульвар Адмирала Ушакова, от центра это 50 минут,  Поляны, 57
    """

    await bot.send_message(message.chat.id, emojize(info_message_1_2))

    video_path_2 = "media/vids/space.mp4"
    if not VIDEO_ID_2:
        msg = await bot.send_video(message.chat.id, InputFile(video_path_2))
        VIDEO_ID_2 = msg.video.file_id
    else:
        await bot.send_video(message.chat.id, VIDEO_ID_2)

    info_message_2 = """
:diamond_shape_with_a_dot_inside: Информационный канал с актуальными новостями о развитии проекта
https://t.me/fluorspaceart
:diamond_shape_with_a_dot_inside: Чат проекта
https://t.me/+oRY3WbYVrtlhYjMy
:diamond_shape_with_a_dot_inside: Twitter
https://twitter.com/FluorSpaceNFT\n
:diamond_shape_with_a_dot_inside: Модерация в чате, запрещены флуд, оскорбления, реклама инвестиционных проектов и т.п.
:diamond_shape_with_a_dot_inside: По всем вопросам пишите:
@Fluor_Space - основатель проекта
@sasaity – куратор
    """

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton("Перейти в канал",
                                          url=f'https://t.me/fluorspaceart'),
               types.InlineKeyboardButton("Перейти в чат",
                                          url=f'https://t.me/+oRY3WbYVrtlhYjMy')]
    for button in buttons:
        keyboard.insert(button)

    await bot.send_message(message.chat.id, emojize(info_message_2), reply_markup=keyboard)

    try:
        await MessageBox.delete_last(message.from_user.id)
    except ValueError as error:
        loguru.logger.error(error)
