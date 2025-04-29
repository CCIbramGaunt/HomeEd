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

def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,)
):
    """
    Parameters request_contact and request_location must be indexes of btns args
    Example:
    get_keyboard(
        'Меню',
        'О магазине',
        'Варианты оплаты',
        'Варианты длоставки',
        'Отправить номер телефона',
        placeholder = 'Что Вас интересует?'
        request_contact = 4,
        sizes = (2,2,1)
    )
    """

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact = True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)



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