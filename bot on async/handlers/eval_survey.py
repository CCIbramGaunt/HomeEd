from aiogram import Bot, types, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from dotenv import find_dotenv, load_dotenv
import os

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from filters.chat_types import ChatTypeFilter

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
bot = Bot(token = TOKEN, default = DefaultBotProperties(parse_mode= ParseMode.HTML))

course_list = {
    '1': 'Курс 1',
    '2': 'Курс 2',
    '3': 'Курс 3',
    '4': 'Курс 4',
    '5': 'Курс 5'
}

eval_survey_router = Router()
eval_survey_router.message.filter(ChatTypeFilter(['private'])) #вызвали фильтр, передав ему список применимых типов сообщений, и применили его к сообщению

class EvaluateCourse(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    course_name = State()
    course_rating = State()
    curator_rating = State()
    materials_rating = State()
    texts = {
        'EvaluateCourse:name': "Пожалуйста, введите свое имя заново",
        'EvaluateCourse:surname': "Пожалуйста, введите свою фамилию заново",
        'EvaluateCourse:phone': "Пожалуйста, введите свой телефон заново",
        'EvaluateCourse:course_name': "Пожалуйста, введите название курса заново",
        'EvaluateCourse:course_rating': "Пожалуйста, введите общую оценку курса заново",
        'EvaluateCourse:curator_rating': "Пожалуйста, введите оценку работы куратора заново",
        'EvaluateCourse:materials_rating': "Пожалуйста, введите оценку материалов курса заново"
    }

@eval_survey_router.message(StateFilter(None), Command('оценить курс'))
@eval_survey_router.message(StateFilter(None), F.text.casefold().contains('оцен'))
async def evaluate_course(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = message.chat.id, text = "На любом шаге Вы можете использовать команду /назад,"
                                                             " чтобы вернуться к предыдущему шагу, либо команду /отмена,"
                                                             " чтобы начать опрос заново" )
    await message.answer("Пожалуйста, введите Ваше имя", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(EvaluateCourse.name)

@eval_survey_router.message(StateFilter('*'), Command("отмена"))
@eval_survey_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены. Воспользуйтесь командой /оценить курс, чтобы начать заново")

@eval_survey_router.message(StateFilter('*'), Command("назад"))
@eval_survey_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == EvaluateCourse.name:
        await message.answer('Предыдущего шага нет. Введите название курса или напишите "отмена"')
        return
    previous = None
    for step in EvaluateCourse.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к предыдущему шагу \n "
                                 f"{EvaluateCourse.texts[previous.state]}")
            return
        previous = step


@eval_survey_router.message(EvaluateCourse.name, F.text)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Пожалуйста, введите Вашу фамилию")
    await state.set_state(EvaluateCourse.surname)

@eval_survey_router.message(EvaluateCourse.name)  # обработка ошибочного ввода (другой тип данных)
async def get_name_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст")

@eval_survey_router.message(EvaluateCourse.surname, F.text)
async def get_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname = message.text)
    await message.answer("Пожалуйста, введите Ваш номер телефона")
    await state.set_state(EvaluateCourse.phone)

@eval_survey_router.message(EvaluateCourse.surname)  # обработка ошибочного ввода (другой тип данных)
async def get_surname_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст")

@eval_survey_router.message(EvaluateCourse.phone, F.text)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone = message.text)
    await message.answer("Какой курс Вы хотели бы оценить? Пожалуйста, укажите цифру")
    await bot.send_message(chat_id = message.chat.id, text = "\n".join(f"{k}: {v}" for k, v in course_list.items()))
    await state.set_state(EvaluateCourse.course_name)

@eval_survey_router.message(EvaluateCourse.phone)  # обработка ошибочного ввода (другой тип данных)
async def get_phone_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите номер цифрами")

@eval_survey_router.message(EvaluateCourse.course_name, F.text)
async def get_course_name(message: types.Message, state: FSMContext):
    try: int(message.text)
    except ValueError: await message.answer("Неверный ввод. Пожалуйста, выберите курс из списка и отправьте его номер")
    else:
        if int(message.text) in range(1, len(course_list)+1):
            await state.update_data(course_name = course_list[message.text])
            await message.answer(f"Пожалуйста, оцените курс {course_list[message.text]} по шкале от 1 до 10")
            await state.set_state(EvaluateCourse.course_rating)
        else: await message.answer("Пожалуйста, выберите курс из списка и отправьте его номер")

@eval_survey_router.message(EvaluateCourse.course_name)  # обработка ошибочного ввода (другой тип данных)
async def get_course_name_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите число")

@eval_survey_router.message(EvaluateCourse.course_rating, F.text)
async def get_course_rating(message: types.Message, state: FSMContext):
    try: int(message.text)
    except ValueError: await message.answer("Неверный ввод. Пожалуйста, оцените курс числом от 1 до 10")
    else:
        if int(message.text) in range(1, 11):
            await state.update_data(course_rating = message.text)
            await message.answer("Пожалуйста, оцените работу куратора по шкале от 1 до 10")
            await state.set_state(EvaluateCourse.curator_rating)
        else: await message.answer("Неверный ввод. Пожалуйста, оцените курс числом от 1 до 10")

@eval_survey_router.message(EvaluateCourse.course_rating)  # обработка ошибочного ввода (другой тип данных)
async def get_course_rating_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст (напишите цифру)")

@eval_survey_router.message(EvaluateCourse.curator_rating, F.text)
async def get_curator_rating(message: types.Message, state: FSMContext):
    try: int(message.text)
    except ValueError: await message.answer("Неверный ввод. Пожалуйста, оцените работу куратора числом от 1 до 10")
    else:
        if int(message.text) in range(1, 11):
            await state.update_data(curator_rating = message.text)
            await message.answer(f"Пожалуйста, оцените учебные материалы по шкале от 1 до 10")
            await state.set_state(EvaluateCourse.materials_rating)
        else: await message.answer("Неверный ввод. Пожалуйста, оцените работу куратора числом от 1 до 10")

@eval_survey_router.message(EvaluateCourse.curator_rating)  # обработка ошибочного ввода (другой тип данных)
async def get_curator_rating_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст (напишите цифру)")

@eval_survey_router.message(EvaluateCourse.materials_rating, F.text)
async def get_materials_rating(message: types.Message, state: FSMContext):
    try: int(message.text)
    except ValueError: await message.answer("Неверный ввод. Пожалуйста, оцените учебные материалы числом от 1 до 10")
    else:
        if int(message.text) in range(1, 11):
            await state.update_data(materials_rating = message.text)
            data = await state.get_data()
            await message.answer("Ваши ответы:\n" +
                             '\nИмя: ' + str(data['name']) + '\nФамилия: ' + str(data['surname']) +
                             '\nТелефон: ' + str(data['phone']) + '\nНазвание курса: ' + str(data['course_name']) +
                             '\nОценка курса: ' + str(data['course_rating']) +
                             '\nОценка работы куратора: ' + str(data['curator_rating']) +
                             '\nОценка учебных материалов: ' + str(data['materials_rating']))
            await bot.send_message(chat_id = message.chat.id, text = "Спасибо за участие в опросе. Вы помогаете нам стать лучше!")
            await bot.send_message(chat_id = message.chat.id, text = 'Нажмите /start для возврата в начало')
            await state.clear()
        else: await message.answer("Неверный ввод. Пожалуйста, оцените учебные материалы числом от 1 до 10")

@eval_survey_router.message(EvaluateCourse.curator_rating)  # обработка ошибочного ввода (другой тип данных)
async def get_curator_rating_check(message: types.Message, state: FSMContext):
    await message.answer("Неверный ввод. Пожалуйста, введите текст (напишите цифру)")