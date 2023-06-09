from telebot import types

kb_city = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1_city = types.KeyboardButton('В Буинск')
bt2_city = types.KeyboardButton('В Казань')
kb_city.add(bt1_city, bt2_city)

kb_day = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1_day = types.KeyboardButton('Сегодня')
bt2_day = types.KeyboardButton('Завтра')
kb_day.add(bt1_day, bt2_day)

kb_part_of_day = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1_part_of_day = types.KeyboardButton('0 - 5')
bt2_part_of_day = types.KeyboardButton('6 - 11')
bt3_part_of_day = types.KeyboardButton('12 - 17')
bt4_part_of_day = types.KeyboardButton('18 - 23')
kb_part_of_day.add(bt1_part_of_day, bt2_part_of_day, bt3_part_of_day, bt4_part_of_day)


kb_time_05 = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1_05 = types.KeyboardButton('00')
bt2_05 = types.KeyboardButton('01')
bt3_05= types.KeyboardButton('02')
bt4_05 = types.KeyboardButton('03')
bt5_05 = types.KeyboardButton('04')
bt6_05 = types.KeyboardButton('05')
kb_time_05.add(bt1_05, bt2_05, bt3_05, bt4_05, bt5_05, bt6_05)