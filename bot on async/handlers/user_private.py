import asyncio
import os
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from dotenv import find_dotenv, load_dotenv
from filters.chat_types import ChatTypeFilter

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private'])) #вызвали фильтр, передав ему список применимых типов сообщений, и применили его к сообщению

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник')

@user_private_router.message(or_f(Command('menu'), (F.text.lower().contains('меню'))))
async def menu_cmd(message: types.Message):
    await message.answer('Ваш id:' + str(message.from_user.id))
    await message.reply('Главное меню:')

@user_private_router.message(Command('evaluate'))
@user_private_router.message(F.text.lower().contains('оцен'))
async def eval_cmd(message: types.Message):
    await message.answer('Здесь запускается скрипт оценки курса')

@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('здесь информация об авторе курсов')

@user_private_router.message(Command('gift'))
@user_private_router.message((F.text.lower() == 'хочу подарок')|(F.text.lower().contains('подар')))
async def gift_cmd(message: types.Message):
    await message.answer('Здесь запускается скрипт получения подарка для посетителей вебинара')