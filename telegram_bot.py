import json
import keyboards
from config import TOKEN_TG
import telebot
from telebot import types

HELLO_MESSAGE = 'Привет!\nЭто бот для поиска попутчиков Буинск - Казань - Буинск. \nКуда вам нужно найти попутчика?'


bot = telebot.TeleBot(TOKEN_TG)


users_in_moment = {}

def update_json(id, key, value):
    with open('db.json', 'r') as file:
        users_in_moment = json.load(file)
    users_in_moment[str(id)][key] = value
    with open('db.json', 'w') as file:
        json.dump(users_in_moment, file, indent=3)


def create_user(id):
    with open('db.json', 'r') as file:
        users_in_moment = json.load(file)
    users_in_moment[id] = {'dest': None, 'day': None, 'time': None}
    with open('db.json', 'w') as file:
        json.dump(users_in_moment, file, indent=3)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, HELLO_MESSAGE, reply_markup=keyboards.kb_city)
    create_user(message.chat.id)
@bot.message_handler(func=lambda message: message.text == 'В Буинск')
def buinsk_choosen_handler(message):
    update_json(message.chat.id, 'dest', 'bua')
    mes = bot.send_message(message.chat.id, 'Отлично! На какой день вам нужна машина?', reply_markup=keyboards.kb_day)
    bot.register_next_step_handler(mes, day_handler)

def day_handler(message):
    if message.text == 'Сегодня':
        update_json(message.chat.id, 'day', 'today')
        mes = bot.send_message(message.chat.id, 'На какое время?', reply_markup=keyboards.kb_part_of_day)
        bot.register_next_step_handler(mes, chose_exact_time)
    elif message.text == 'Завтра':
        update_json(message.chat.id, 'day', 'tommorow')
        mes = bot.send_message(message.chat.id, 'На какое время?')
        bot.register_next_step_handler(mes, chose_exact_time)
    else:
        bot.send_message(message.chat.id, 'Уточните день')

def chose_exact_time(message):
    text = message.text.split(' - ')
    start = int(text[0])
    end = int(text[1])
    kb_exact_time = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(start, end + 1):
        if i < 10:
            kb_exact_time.add(types.KeyboardButton(f'0{str(i)}:00'))
        else:
            kb_exact_time.add(types.KeyboardButton(f'{str(i)}:00'))
    mes = bot.send_message(message.chat.id, 'Точное время', reply_markup=kb_exact_time)
    bot.register_next_step_handler(mes, final_handler)


def final_handler(message):
    update_json(message.chat.id, 'time', message.text)
    bot.send_message(message.chat.id, 'Принял!')
bot.polling()