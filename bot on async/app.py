import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import os
from dotenv import find_dotenv, load_dotenv

allowed_updates = ['message, edited_message']

load_dotenv(find_dotenv())
from handlers.user_private import user_private_router
TOKEN = os.getenv("TOKEN")
bot = Bot(token = TOKEN)
disp = Dispatcher()

disp.include_router(user_private_router)

async def main():
    await bot.delete_webhook(drop_pending_updates = True)
    await disp.start_polling(bot, allowed_updates = allowed_updates)

asyncio.run(main())