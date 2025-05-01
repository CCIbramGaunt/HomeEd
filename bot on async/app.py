import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import os

from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv

allowed_updates = ['message, edited_message']

load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from handlers.admin_private import admin_router
from handlers.eval_survey import eval_survey_router
from common.bot_cmnds_list import private

TOKEN = os.getenv("TOKEN")
bot = Bot(token = TOKEN, default = DefaultBotProperties(parse_mode= ParseMode.HTML))

disp = Dispatcher()

disp.include_router(user_private_router)
disp.include_router(eval_survey_router)
disp.include_router(user_group_router)
disp.include_router(admin_router)

async def main():
    await bot.delete_webhook(drop_pending_updates = True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands = private, scope = types.BotCommandScopeAllPrivateChats())
    await disp.start_polling(bot, allowed_updates = allowed_updates)

asyncio.run(main())