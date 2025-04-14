import telebot
import os
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
namelist = []
clients = {}
ratings_list = {}
client_id = ''
func_queue = 0

TOKEN = os.getenv("TOKEN")
my_bot = telebot.TeleBot(TOKEN)

@my_bot.message_handler(content_types=['text'])
def start(message):
    global client_id, clients
    client_id = message.chat.id
    clients[client_id] = {}
    if message.text == '/start':
        my_bot.send_message(client_id, "Здравствуйте. Как Вас зовут?")
        my_bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        my_bot.send_message(client_id, 'Я Вас не понимаю. Пожалуйста, напишите /start для оценки курса')

def get_name(message):          #получаем имя
    global client_id
    name = message.text
    clients['client_id'] = client_id
    clients[client_id]['name'] = name
    my_bot.send_message(client_id, f'{name}, пожалуйста, введите Вашу фамилию')
    my_bot.register_next_step_handler(message, get_surname)

def get_surname(message): #получаем фамилию
    global client_id
    surname = message.text
    clients[client_id]['surname'] = surname
    my_bot.send_message(client_id, f'Введите, пожалуйста, Ваш номер телефона')
    my_bot.register_next_step_handler(message, get_phone)

def get_phone(message): #получаем фамилию
    global client_id
    phone = message.text
    clients[client_id]['phone'] = phone
    name =  clients[client_id]['name']
    my_bot.send_message(client_id, f'{name}, какой курс Вы хотели бы оценить?')
    my_bot.register_next_step_handler(message, get_course_name)

def errors(message):
    global client_id
    name =  clients[client_id]['name']
    if message.text == f'{name}, кажется, я Вас неправильно понял. Попробую снова.':
        my_bot.send_message(client_id, 'Какой курс Вы хотели бы оценить?')
        my_bot.register_next_step_handler(message, get_course_name)

def get_course_name(message):
    global client_id
    course_name = message.text
    clients[client_id]['course_name'] = course_name
    name =  clients[client_id]['name']
    my_bot.send_message(client_id, f'{name}, на сколько баллов Вы оцениваете этот курс, от 0 до 10?')
    my_bot.register_next_step_handler(message, get_rating_0)

def function_name_cycler(func):  # получает функцию и возвращает ее имя (СТРОКУ!!!) с увеличенным на 1 последним символом
    global client_id
    # my_bot.send_message(client_id, f'Декоратор function_name_cycler. работаю с {func.__name__}.')
    func_queue_index = int(func.__name__[-1]) + 1
    next_func_name = func.__name__[0:-1] + str(func_queue_index)
    return next_func_name



def response_checker(func):
    def wrapper(*args):
        global client_id
        # my_bot.send_message(client_id, f'Декоратор. работаю с {func.__name__}.')
        try:
            # my_bot.send_message(client_id, f'начинаю блок try декоратора')
            int(args[0].text)  # проверяем, что оценка - это целое число
        except Exception:
            request = my_bot.send_message(client_id, f'Пожалуйста, поставьте оценку числом')
            my_bot.register_next_step_handler(request, wrapper)
            return # wrapper(args[0])
        else:
            if int(args[0].text) not in range(0,11):
                request = my_bot.send_message(client_id, f'Пожалуйста, поставьте оценку от 0 до 10.')
                my_bot.register_next_step_handler(request, wrapper)
            else:
                func(*args)
                my_bot.register_next_step_handler(args[0], functions_dictionary[function_name_cycler(func)])


    return wrapper# Возвращает None

@response_checker
def get_rating_0(message):          #получаем оценку курса
    global client_id
    # my_bot.send_message(client_id, f'старт функции get_rating_0')
    clients[client_id]['course_rating'] = int(message.text)
    my_bot.send_message(client_id, 'Пожалуйста, оцените работу куратора 0 до 10')
    return int(message.text)

@response_checker
def get_rating_1(message):          #получаем оценку куратора
    global client_id
    # my_bot.send_message(client_id, f'старт функции get_rating_1')
    clients[client_id]['curator_rating'] = int(message.text)
    my_bot.send_message(client_id, 'Пожалуйста, оцените учебные материалы курса от 0 до 10')
    # my_bot.register_next_step_handler(message, get_rating_2)
    return int(message.text)

@response_checker
def get_rating_2(message):          #получаем оценку материала
    global client_id
    # my_bot.send_message(client_id, f'старт функции get_rating_2')
    clients[client_id]['material_rating'] = int(message.text)
    my_bot.send_message(client_id, 'Насколько вероятно, что Вы порекомендуете пройти этот курс друзьям? От 0 до 10')
    # my_bot.register_next_step_handler(message, get_rating_3)
    return int(message.text)

@response_checker
def get_rating_3(message):          #получаем вероятность рекомендации
    global client_id
    # my_bot.send_message(client_id, f'старт функции get_rating_3')
    clients[client_id]['recommendation_rating'] = int(message.text)
    get_rating_4()
    return int(message.text)

def get_rating_4():
        global client_id
        course_name = clients[client_id]['course_name']
        course_rating = clients[client_id]['course_rating']
        curator_rating = clients[client_id]['curator_rating']
        material_rating = clients[client_id]['material_rating']
        name = clients[client_id]['name']
        surname = clients[client_id]['surname']
        keyboard = InlineKeyboardMarkup()  # наша клавиатура
        key_yes = InlineKeyboardButton(text='Да', callback_data='correct')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = InlineKeyboardButton(text='Нет, изменить', callback_data='incorrect')
        keyboard.add(key_no)
        my_bot.send_message(client_id, f'{name}, позвольте мне уточнить')
        question =  (f'Ваши оценки курса {course_name}:\n'
                     f'Общая оценка - {course_rating},\n'
                     f'Оценка работы куратора - {curator_rating},\n'
                     f'Оценка учебных материалов - {material_rating},\n'
                     f'верно?')

        my_bot.send_message(client_id, text=question, reply_markup=keyboard)

functions_dictionary = {
    'start': start,
    'get_name': get_name,
    'get_surname': get_surname,
    'get_phone': get_phone,
    'errors': errors,
    'get_course_name': get_course_name,
    'function_name_cycler': function_name_cycler,
    'response_checker': response_checker,
    'get_rating_0': get_rating_0,
    'get_rating_1': get_rating_1,
    'get_rating_2': get_rating_2,
    'get_rating_3': get_rating_3,
    'get_rating_4': get_rating_4
}

@my_bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    global client_id
    name = clients[client_id]['name']
    match call.data:
        case 'correct':
            my_bot.send_message(call.message.chat.id, f'Спасибо за оценку, {name}')
            my_bot.answer_callback_query(callback_query_id=call.id, text=f'Благодарю за Вашу за оценку, {name}. Ваш отзыв важен для нас, он помогает нам стать лучше')
            with open('clients list.txt', 'a+') as file:
                for key, value in clients[client_id].items():
                    file.write(f'{client_id}:%s:%s\n' % (key, value))
            file.close()
            message = my_bot.send_message(call.message.chat.id, f'Пожалуйста, используйте /start для оценки курса')
            my_bot.register_next_step_handler(message, start)
        case 'incorrect':
            # my_bot.answer_callback_query(callback_query_id=call.id, text='Ошибка')
            message = my_bot.send_message(call.message.chat.id, f'{name}, кажется, я Вас неправильно понял. Попробую снова.')
            errors(message)
my_bot.infinity_polling()