import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник')

@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message, bot: Bot):
    await message.answer('Ваш id:' + str(message.from_user.id))
    await message.reply('Главное меню:')

@user_private_router.message(Command('evaluate'))
async def eval_cmd(message: types.Message, bot: Bot):
    await message.answer('Здесь запускается скрипт оценки курса')

@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message, bot: Bot):
    await message.answer('здесь информация об авторе курсов')

@user_private_router.message(Command('gift'))
async def gift_cmd(message: types.Message, bot: Bot):
    await message.answer('Здесь запускается скрипт получения подарка')