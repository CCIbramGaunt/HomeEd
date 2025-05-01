from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
import os

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import find_dotenv, load_dotenv


from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard

load_dotenv(find_dotenv())

admins_list = list(map(int, os.getenv("admins_list").split(',')))
admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin(admins_list))

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

class AddCourse(StatesGroup):
    name = State()
    description = State()
    price = State()
    notes = State()
    texts = {
        'AddCourse:name': "Введите название заново",
        'AddCourse:description': "Введите описание заново",
        'AddCourse:price': "Введите стоимость заново",
        'AddCourse:notes': "Введите доп инфо заново",
    }

@admin_router.message(StateFilter(None), F.text == "Добавить курс")
async def add_course(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название курса", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddCourse.name)

@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup = ADMIN_KB)

@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddCourse.name:
        await message.answer('Предыдущего шага нет. Введите название курса или напишите "отмена"')
        return
    previous = None
    for step in AddCourse.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к предыдущему шагу \n "
                                 f"{AddCourse.texts[previous.state]}")
            return
        previous = step

@admin_router.message(AddCourse.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Введите описание нового курса")
    await state.set_state(AddCourse.description)

@admin_router.message(AddCourse.name)  # обработка ошибочного ввода (другой тип данных)
async def add_name_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст")

@admin_router.message(AddCourse.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость нового курса")
    await state.set_state(AddCourse.price)

@admin_router.message(AddCourse.description)
async def add_description_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст")

@admin_router.message(AddCourse.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price = message.text)
    await message.answer("Введите дополнительную информацию (доступность, рассрочка, скидка, время...)")
    await state.set_state(AddCourse.notes)

@admin_router.message(AddCourse.price)
async def add_price_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст")

@admin_router.message(AddCourse.notes, F.text)
async def add_notes(message: types.Message, state: FSMContext):
    await state.update_data(notes = message.text)
    await message.answer("Курс добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

@admin_router.message(AddCourse.notes)
async def add_notes_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст")

