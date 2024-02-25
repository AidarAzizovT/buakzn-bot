import datetime
import json
import keyboards
from config import TOKEN_TG
import telebot
import logging
from time import sleep
from telebot import types
from get_info_from_vk import search_for_tommorow_passenger, \
    search_for_today_passenger, search_for_today_driver, search_for_tommorow_driver
import re
from random import randint

HELLO_MESSAGE = 'Привет!\nЭто бот для поиска попутчиков Буинск - Казань - Буинск. \nЧто вы ищите?'
ad_channel = 'https://t.me/bmchn'

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
    users_in_moment[id] = {'action': None, 'dest': None, 'day': None, 'time': None}
    with open('db.json', 'w') as file:
        json.dump(users_in_moment, file, indent=3)


def delete_user_from_json(id):
    with open('db.json', 'r') as file:
        users_in_moment = json.load(file)
    if str(id) in users_in_moment.keys():
        del users_in_moment[str(id)]
    with open('db.json', 'w') as file:
        json.dump(users_in_moment, file, indent=3)


def get_data_from_json(id):
    with open('db.json', 'r') as file:
        users_in_moment = json.load(file)
    if str(id) in users_in_moment.keys():
        return users_in_moment[str(id)]
    else:
        return None


def make_sendable(data):
  if data == None:
    return ''
  else:
    for_send = ''
    for elem in data[:10]:
      for_send += f'Дата публикации: {elem["published_date"].strftime("%d/%m - %H:%M")}\n'
      updated_text = re.sub(r'\b8(?=\d{10}\b)', r'+7', elem["text"])
      for_send += f"{updated_text}\n"
      for_send += f'Ссылка на человека: {elem["link_to_publisher"]}'
      for_send += '\n\n'
    return for_send


@bot.message_handler(commands=['start'])
def start_handler(message):
    mes = bot.send_message(message.chat.id, HELLO_MESSAGE, reply_markup=keyboards.kb_action)
    create_user(message.chat.id)
    bot.register_next_step_handler(mes, action_handler)

@bot.message_handler(func=lambda message: message.text == 'Выбрать действие')
def action_handler(message):
    if message.text in ['Я ищу машину (водителя)', 'Я ищу людей (пассажиров)']:
        update_json(message.chat.id, 'action', message.text)
        mes = bot.send_message(message.chat.id, 'Хорошо! Куда едем?', reply_markup=keyboards.kb_city)
        bot.register_next_step_handler(mes, city_handler)


    else:
        mes = bot.send_message(message.chat.id, 'Я вас не понял\nДавайте начнём заново?',
                               reply_markup=keyboards.kb_again)
        bot.register_next_step_handler(mes, again_handler)
def city_handler(message):
    if message.text == 'В Буинск':
        update_json(message.chat.id, 'dest', 'в буинск')
        mes = bot.send_message(message.chat.id, 'Отлично! На какой день?',
                               reply_markup=keyboards.kb_day)
        bot.register_next_step_handler(mes, day_handler)
    elif message.text == 'В Казань':
        update_json(message.chat.id, 'dest', 'в казань')
        mes = bot.send_message(message.chat.id, 'Отлично! На какой день вам нужна машина?',
                               reply_markup=keyboards.kb_day)
        bot.register_next_step_handler(mes, day_handler)

    elif message.text == 'Начать заново':
        bot.send_message(message.chat.id, 'Хорошо, давайте начнём заново.', reply_markup=keyboards.kb_choose_action)

    else:
        mes = bot.send_message(message.chat.id, 'Я вас не понял\nДавайте начнём заново?', reply_markup=keyboards.kb_again)
        bot.register_next_step_handler(mes, again_handler)


def day_handler(message):
    if message.text == 'Сегодня':
        update_json(message.chat.id, 'day', 'today')
        mes = bot.send_message(message.chat.id, 'На какое время?', reply_markup=keyboards.kb_part_of_day)
        bot.register_next_step_handler(mes, chose_exact_time)
    elif message.text == 'Завтра':
        update_json(message.chat.id, 'day', 'tommorow')
        mes = bot.send_message(message.chat.id, 'На какое время?', reply_markup=keyboards.kb_part_of_day)
        bot.register_next_step_handler(mes, chose_exact_time)
    else:
        mes = bot.send_message(message.chat.id, 'Я вас не понял\nДавайте начнём заново?',
                               reply_markup=keyboards.kb_again)
        bot.register_next_step_handler(mes, again_handler)

def chose_exact_time(message):
    pattern = r'^([01]\d|2[0-3]):[0-5]\d - ([01]\d|2[0-3]):[0-5]\d$'
    if re.match(pattern, message.text):
        times = message.text.split(' - ')
        start = int(times[0][0:-3])
        end = int(times[1][0:-3])
        print(start, end)
        kb_exact_time = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(start, end + 1):
            if i < 10:
                kb_exact_time.add(types.KeyboardButton(f'0{str(i)}:00'))
            else:
                kb_exact_time.add(types.KeyboardButton(f'{str(i)}:00'))
        mes = bot.send_message(message.chat.id, 'Точное время', reply_markup=kb_exact_time)
        bot.register_next_step_handler(mes, final_handler)
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не смог найти объявлений по вашему запросу :(',
                         reply_markup=keyboards.kb_again)
        delete_user_from_json(message.chat.id)


def final_handler(message):
    pattern = '^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, message.text):
        update_json(message.chat.id, 'time', message.text)
        data_of_user = get_data_from_json(message.chat.id)
        if data_of_user['action'] == 'Я ищу машину (водителя)':
            if data_of_user['day'] == 'today':
                data = search_for_today_passenger(data_of_user['time'], data_of_user['dest'])
                data = make_sendable(data)
                if len(data) != 0:
                    bot.send_message(message.chat.id, data)
                    bot.send_message(message.chat.id, 'Надеюсь, смог вам помочь!', reply_markup=keyboards.kb_again)
                else:
                    bot.send_message(message.chat.id, 'К сожалению, я не смог найти объявлений по вашему запросу :(', reply_markup=keyboards.kb_again)
                delete_user_from_json(message.chat.id)

            elif data_of_user['day'] == 'tommorow':
                data = search_for_tommorow_passenger(data_of_user['time'], data_of_user['dest'])
                data = make_sendable(data)
                print(data)
                if len(data) != 0:
                    bot.send_message(message.chat.id, data)
                    bot.send_message(message.chat.id, 'Надеюсь, смог вам помочь!', reply_markup=keyboards.kb_again)
                else:
                    bot.send_message(message.chat.id, 'К сожалению, я не смог найти объявлений по вашему запросу :(',
                                     reply_markup=keyboards.kb_again)
                delete_user_from_json(message.chat.id)
            else:
                mes = bot.send_message(message.chat.id, 'Я вас не понял\nДавайте начнём заново?',
                                       reply_markup=keyboards.kb_again)
                delete_user_from_json(message.chat.id)
                bot.register_next_step_handler(mes, again_handler)
        elif data_of_user['action'] == 'Я ищу людей (пассажиров)':
            if data_of_user['day'] == 'today':
                data = search_for_today_driver(data_of_user['time'], data_of_user['dest'])
                data = make_sendable(data)
                if len(data) != 0:
                    bot.send_message(message.chat.id, data)
                    bot.send_message(message.chat.id, 'Надеюсь, смог вам помочь!', reply_markup=keyboards.kb_again)
                else:
                    bot.send_message(message.chat.id, 'К сожалению, я не смог найти объявлений по вашему запросу :(',
                                     reply_markup=keyboards.kb_again)
                delete_user_from_json(message.chat.id)

            elif data_of_user['day'] == 'tommorow':
                data = search_for_tommorow_driver(data_of_user['time'], data_of_user['dest'])
                data = make_sendable(data)
                print(data)
                if len(data) != 0:
                    bot.send_message(message.chat.id, data)
                    bot.send_message(message.chat.id, 'Надеюсь, смог вам помочь!', reply_markup=keyboards.kb_again)
                else:
                    bot.send_message(message.chat.id, 'К сожалению, я не смог найти объявлений по вашему запросу :(',
                                     reply_markup=keyboards.kb_again)
                delete_user_from_json(message.chat.id)
            else:
                mes = bot.send_message(message.chat.id, 'Я вас не понял\nДавайте начнём заново?',
                                       reply_markup=keyboards.kb_again)
                delete_user_from_json(message.chat.id)
                bot.register_next_step_handler(mes, again_handler)
    else:
        gif = open(f'gifs/gif_{randint(1, 6)}.mp4', 'rb')
        bot.send_animation(message.chat.id, gif, reply_markup=keyboards.kb_again)



@bot.message_handler(func=lambda mes: mes.text == 'Начать заново')
def again_handler(message):
    create_user(message.chat.id)
    mes = bot.send_message(message.chat.id, 'Что вы ищите?', reply_markup=
                           keyboards.kb_action)
    bot.register_next_step_handler(mes, action_handler)

@bot.message_handler()
def handler_of_all_other_messages(message):
    MES = 'К сожалению, я вас не понимаю, ' \
          'пока что я могу лишь помогать находить попутчиков :)\n' \
          'Может быть вам нужно именно это?'
    sent_mes = bot.send_message(message.chat.id, MES, reply_markup=keyboards.kb_yes_no)
    bot.register_next_step_handler(sent_mes, yes_no_handler)

def yes_no_handler(message):
    if message.text == 'Да':
        mes = bot.send_message(message.chat.id, 'Отлично! Что вы ищите?', reply_markup=keyboards.kb_action)
        create_user(message.chat.id)
        bot.register_next_step_handler(mes, action_handler)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id,  f'Тогда, к сожалению, я не смогу вам помочь :( \nМожете подписаться на канал наших друзей {ad_channel}', reply_markup=keyboards.kb_again)

    else:
        gif = open(f'gifs/gif_{randint(1, 6)}.mp4', 'rb')
        bot.send_animation(message.chat.id, gif, reply_markup=keyboards.kb_again)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='logs.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        logging.error(f"Error occurred: {e}", exc_info=True)
        sleep(2)