import asyncio
import os
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from dotenv import find_dotenv, load_dotenv


from filters.chat_types import ChatTypeFilter
from keyboards.reply import get_keyboard

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private'])) #вызвали фильтр, передав ему список применимых типов сообщений, и применили его к сообщению

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        'Привет, я виртуальный помощник',
             reply_markup = get_keyboard(
                'Меню',
                'Оценка курса',
                'Варианты оплаты',
                'Варианты обучения',
                placeholder = 'Что Вас интересует?',
                sizes = (2,2)
             )
    )


@user_private_router.message(or_f(Command('menu'), (F.text.lower().contains('меню'))))
async def menu_cmd(message: types.Message):
    await message.reply('Главное меню:')

@user_private_router.message(Command('evaluate'))
@user_private_router.message(F.text.lower().contains('оцен'))
async def eval_cmd(message: types.Message):
    text = as_marked_section(
        Bold('Курсы, доступные для оценки:'),
        'Первый',
        'Второй',
        'Третий',
        'Четвертый',
        marker = '✅ '
    )
    await message.answer(text.as_html())

@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('здесь информация об авторе курсов')

@user_private_router.message(Command('gift'))
@user_private_router.message((F.text.lower() == 'хочу подарок')|(F.text.lower().contains('подар')))
async def gift_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Подарки, доступные для получения:'),
            'Первый',
            'Второй',
            'Третий',
            'Четвертый',
            marker='✅ '
        ),
        as_marked_section(
            Bold('Подарки, которые еще можно успеть получить:'),
            'Первый',
            'Второй',
            'Третий',
            'Четвертый',
            marker='🏃‍♂️‍➡️ '
        ),
        as_marked_section(
            Bold('Подарки, которые уже закончились'),
            'Первый',
            'Второй',
            'Третий',
            'Четвертый',
            marker='🤷‍♂️ '
        ),
        sep = '\n------------\n'
    )
    await message.answer(text.as_html())

@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f'Номер получен')
    await message.answer(str(message.contact))

@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f'Локация получена')
    await message.answer(str(message.location))
