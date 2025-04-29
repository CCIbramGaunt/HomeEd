from aiogram import F, Router, types
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить курс",
    "Изменить курс",
    "Удалить курс",
    "Тест",
    placeholder = "Выберите действие",
    sizes = (2,1,1),
)


@admin_router.message(Command("admin"))
async def admin_cmd(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup = ADMIN_KB)

@admin_router.message(F.text == "Тест")
async def test_cmd(message: types.Message):
    await message.answer("ОК. Вот текущий список курсов")

@admin_router.message(F.text == "Изменить курс")
async def change_cmd(message: types.Message):
    await message.answer("ОК. Вот текущий список курсов")

@admin_router.message(F.text == "Удалить курс")
async def delete_cmd(message: types.Message):
    await message.answer("ОК. Выберите курс(ы) для удаления")

#  Начинаем работу с машиной состояний


