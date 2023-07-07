from telebot import types
bt_again = bt1 = types.KeyboardButton('Начать заново')


kb_city = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1_city = types.KeyboardButton('В Буинск')
bt2_city = types.KeyboardButton('В Казань')
kb_city.add(bt1_city, bt2_city, bt_again)

kb_day = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1_day = types.KeyboardButton('Сегодня')
bt2_day = types.KeyboardButton('Завтра')
kb_day.add(bt1_day, bt2_day, bt_again)

kb_part_of_day = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
bt1_part_of_day = types.KeyboardButton('00:00 - 05:00')
bt2_part_of_day = types.KeyboardButton('06:00 - 11:00')
bt3_part_of_day = types.KeyboardButton('12:00 - 17:00')
bt4_part_of_day = types.KeyboardButton('18:00 - 23:00')
kb_part_of_day.add(bt1_part_of_day, bt2_part_of_day, bt3_part_of_day, bt4_part_of_day, bt_again)


kb_action = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1 = types.KeyboardButton('Я ищу машину (водителя)')
bt2 = types.KeyboardButton('Я ищу людей (пассажиров)')
kb_action.add(bt1, bt2)

kb_again = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1 = types.KeyboardButton('Начать заново')
kb_again.add(bt1)

kb_yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1 = types.KeyboardButton('Да')
bt2 = types.KeyboardButton('Нет')
kb_yes_no.add(bt1, bt2)

kb_choose_action = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt = types.KeyboardButton('Выбрать действие')
kb_choose_action.add(bt)


kb_sure = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1 = types.KeyboardButton('Да, я уверен')
bt2 = types.KeyboardButton('Я ошибся')
kb_sure.add(bt1, bt2)