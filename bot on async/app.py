import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

bot = Bot(token='7633105953:AAHf383wggpu0PSz7WtfiRbxpAbGffJNcjE')
disp = Dispatcher()

@disp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('это была команда старт')

@disp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    await disp.start_polling(bot)

asyncio.run(main())