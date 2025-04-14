import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

name = ''
course_name = ''
course_rating = 0
ratings_list = {}
client_id = 0

my_bot = telebot.TeleBot('7633105953:AAHf383wggpu0PSz7WtfiRbxpAbGffJNcjE')

@my_bot.message_handler(content_types=['text'])
def start(message):
    global client_id
    client_id = message.from_user.id
    if message.text == '/start':
        my_bot.send_message(client_id, f"Я только что получил сообщение {message.text}")
        my_bot.send_message(client_id, "Здравствуйте. Как Вас зовут?")
        my_bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        my_bot.send_message(client_id, 'Я Вас не понимаю. Пожалуйста, напишите /start для оценки курса')

def get_name(message): #получаем фамилию
    global name
    name = message.text
    my_bot.send_message(client_id, 'Какой курс Вы хотели бы оценить?')
    my_bot.register_next_step_handler(message, get_course_name)

def errors(message):
    if message.text == f'Кажется, я Вас неправильно понял, {name}. Попробую снова.':
        my_bot.send_message(client_id, 'Какой курс Вы хотели бы оценить?')
        my_bot.register_next_step_handler(message, get_course_name)

def get_course_name(message):
    global course_name
    course_name = message.text
    my_bot.send_message(client_id, 'На сколько баллов Вы оцениваете этот курс, от 0 до 10? метка 1')
    my_bot.register_next_step_handler(message, check_course_rating_response_1)

def check_course_rating_response_1(message):
    global course_rating
    try: course_rating = int(message.text)  # проверяем, что оценка - это целое число
    except Exception:
        my_bot.send_message(client_id, 'Пожалуйста, оцените курс числом от 0 до 10 метка 2')
        my_bot.register_next_step_handler(message, check_course_rating_response_2)
        return False
    if course_rating not in range(0,11):
        my_bot.send_message(client_id, 'Пожалуйста, оцените курс числом от 0 до 10 метка 3')
        my_bot.register_next_step_handler(message, check_course_rating_response_2)
        return False
    else:
        course_rating = int(message.text)
        get_course_rating()
        my_bot.send_message(client_id, 'Готов записать оценку курса')
        return course_rating

def check_course_rating_response_2(message):
    global course_rating
    try: course_rating = int(message.text)  # проверяем, что оценка - это целое число
    except Exception:
        my_bot.send_message(client_id, 'Пожалуйста, оцените курс числом от 0 до 10 метка 4')
        my_bot.register_next_step_handler(message, check_course_rating_response_1)
        return False
    if course_rating not in range(0,11):
        my_bot.send_message(client_id, 'Пожалуйста, оцените курс числом от 0 до 10 метка 5')
        my_bot.register_next_step_handler(message, check_course_rating_response_1)
        return False
    else:
        course_rating = int(message.text)
        get_course_rating()
        my_bot.send_message(client_id, 'Готов записать оценку курса')
        return course_rating

def get_course_rating():
        keyboard = InlineKeyboardMarkup()  # наша клавиатура
        key_yes = InlineKeyboardButton(text='Да', callback_data='correct')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = InlineKeyboardButton(text='Нет', callback_data='incorrect')
        keyboard.add(key_no)
        question = f'Вы оценили курс {course_name} на {course_rating} баллов из 10, верно?'
        my_bot.send_message(client_id, text=question, reply_markup=keyboard)

@my_bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    match call.data:
        case 'correct':
            my_bot.send_message(call.message.chat.id, 'Спасибо за Вашу оценку')
            my_bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за оценку')
            start(client_id, 'return')
        case 'incorrect':
            my_bot.answer_callback_query(callback_query_id=call.id, text='Ошибка')
            message = my_bot.send_message(call.message.chat.id, f'Кажется, я Вас неправильно понял, {name}. Попробую снова.')
            errors(message)
my_bot.infinity_polling()