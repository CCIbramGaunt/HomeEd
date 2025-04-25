from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButtonPollType

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Главное меню'),
            KeyboardButton(text = 'Подарок для слушателей вебинара')
        ],
        [
            KeyboardButton(text = 'Оценить курс'),
            KeyboardButton(text = 'Об авторе курсов')
        ]
    ],
    resize_keyboard = True,
    input_field_placeholder = 'Что Вас интересует?'
)

del_kb = ReplyKeyboardRemove()

start_kb_2 = ReplyKeyboardBuilder()
start_kb_2.add(
            KeyboardButton(text = 'Главное меню'),
            KeyboardButton(text = 'Подарок для слушателей вебинара'),
            KeyboardButton(text = 'Оценить курс'),
            KeyboardButton(text = 'Об авторе курсов')
)
start_kb_2.adjust(2,2)

start_kb_3 = ReplyKeyboardBuilder()
start_kb_3.attach(start_kb_2)
start_kb_3.row(KeyboardButton(text = 'Посмотреть доступные курсы'))

test_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = 'Создать опрос', request_poll = KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text = 'Отправить контакт ☎️', request_contact = True),
            KeyboardButton(text = 'Отправить локацию 🗺️', request_location = True)
        ],
    ],
    resize_keyboard = True,
)