import telebot
import datetime
from telebot import types
import sqlite3


bot = telebot.TeleBot('5120863127:AAEGrwvIoC9f9OG6JT3d5KJm7Hp8PE3nBdI')
game_check = 0
prac_numb = 0
con = sqlite3.connect("first.sqlite", check_same_thread=False)
cur = con.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    global game_check
    game_check = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Новая тренировка")
    btn2 = types.KeyboardButton("Новая игра")
    btn3 = types.KeyboardButton("Тренировка")
    btn4 = types.KeyboardButton("Игра")
    btn5 = types.KeyboardButton("Удаление тренировки")
    btn6 = types.KeyboardButton("Удаление игры")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "hockey team", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global game_check, prac_numb
    n = '\n'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Новая тренировка':
        g = cur.execute(f"""SELECT id FROM first;""").fetchall()
        if g:
            for i in g:
                prac_numb = int(str(i[0])) + 1
        else:
            prac_numb = 1
        bot.send_message(message.chat.id, text='Напишите дату тренировки в формате DD.MM.YYYY')
        game_check = 1
    elif message.text == "Вернуться в главное меню":
        start(message)
        game_check = 0
    elif game_check == 1:
        try:
            d = message.text.split('.')
            date = datetime.date(int(d[2]), int(d[1]), int(d[0]))
            game_check = 2
            cur.execute(f"""INSERT INTO first(id, info, names, date) VALUES({prac_numb}, '', '', '{date}')""").fetchall()
            con.commit()
            bot.send_message(message.chat.id, text='Напишите информацию о тренировке:')
        except:
            bot.send_message(message.chat.id, text='Неверный формат даты, попробуйте еще раз.')
            game_check = 1
    elif game_check == 2:
        d = message.text
        game_check = 0
        cur.execute(f"""UPDATE first SET info = '{d}' WHERE id = {prac_numb}""").fetchall()
        con.commit()
    elif message.text == 'Удаление тренировки':
        game_check = 8
        g = cur.execute(f"""SELECT * FROM first;""").fetchall()
        s = ''
        for i in g:
            s = s + f'Тренировка номер {i[0]}, информация о тренировке: {i[1]}, дата тренировки: {i[3]}{n}'
        if s == '':
            bot.send_message(message.chat.id, text='Тренировок в списке нет.')
            game_check = 0
        else:
            s = s + 'Введите номер тренировки чтобы удалить ее.'
            bot.send_message(message.chat.id, text=s)
    elif game_check == 8:
        game_check = 0
        try:
            d = int(message.text)
            cur.execute(f"""DELETE from first  WHERE id = {d}""").fetchall()
            con.commit()
            bot.send_message(message.chat.id, text='Тренировка удалена.')
        except:
            bot.send_message(message.chat.id, text='Не корректное число.')
    elif message.text == 'Удаление игры':
        game_check = 7
        g = cur.execute(f"""SELECT * FROM game;""").fetchall()
        s = ''
        for i in g:
            s = s + f'Игра номер {i[0]}, информация о игре: {i[1]}, дата игры: {i[3]}{n}'
        if s == '':
            bot.send_message(message.chat.id, text='Игр в списке нет.')
            game_check = 0
        else:
            s = s + 'Введите номер игры чтобы удалить ее.'
            bot.send_message(message.chat.id, text=s)
    elif game_check == 7:
        game_check = 0
        try:
            d = int(message.text)
            cur.execute(f"""DELETE from game WHERE id = {d}""").fetchall()
            con.commit()
            bot.send_message(message.chat.id, text='Игра удалена.')
        except:
            bot.send_message(message.chat.id, text='Не корректное число.')

    elif message.text == 'Новая игра':
        g = cur.execute(f"""SELECT id FROM game;""").fetchall()
        if g:
            for i in g:
                prac_numb = int(str(i[0])) + 1
        else:
            prac_numb = 1
        bot.send_message(message.chat.id, text='Напишите дату тренировки в формате DD.MM.YYYY')
        game_check = 3
    elif game_check == 3:
        try:
            d = message.text.split('.')
            date = datetime.date(int(d[2]), int(d[1]), int(d[0]))
            game_check = 4
            cur.execute(f"""INSERT INTO game(id, info, names, date) VALUES({prac_numb}, '', '', '{date}')""").fetchall()
            con.commit()
            bot.send_message(message.chat.id, text='Напишите информацию о тренировке:')
        except:
            bot.send_message(message.chat.id, text='Неверный формат даты, попробуйте еще раз.')
            game_check = 3
    elif game_check == 4:
        d = message.text
        game_check = 0
        cur.execute(f"""UPDATE game SET info = '{d}' WHERE id = {prac_numb}""").fetchall()
        con.commit()
    elif message.text == 'Игра':
        g = cur.execute(f"""SELECT * FROM game;""").fetchall()
        s = ''
        game_check = 6
        for i in g:
            d = datetime.datetime.strptime(i[3], '%Y-%m-%d')
            today = datetime.datetime.now()
            if (d - today).days >= 0 and (d - today).days < 30:
                s = s + f'Игра номер {i[0]}, информация о игре: {i[1]}, дата игры: {i[3]}{n}'
        if s == '':
            bot.send_message(message.chat.id, text='Игр в ближайшее время нет.')
            game_check = 0
        else:
            s = s + 'Введите номер игры:'
            bot.send_message(message.chat.id, text=s)
    elif message.text == 'Тренировка':
        g = cur.execute(f"""SELECT * FROM first;""").fetchall()
        s = ''
        game_check = 5
        for i in g:
            d = datetime.datetime.strptime(i[3], '%Y-%m-%d')
            today = datetime.datetime.now()
            if (d - today).days >= 0 and (d - today).days < 7:
                s = s + f'Тренировка номер {i[0]}, информация о тренировке: {i[1]}, дата тренировки: {i[3]}{n}'
        if s == '':
            bot.send_message(message.chat.id, text='Тренировок в ближайшее время нет.')
            game_check = 0
        else:
            s = s + 'Введите номер тренировки:'
            bot.send_message(message.chat.id, text=s)
    elif game_check == 5:
        s = ''
        game_check = 0
        try:
            prac_numb = int(message.text)
            g = cur.execute(f"""SELECT * FROM first WHERE id = {prac_numb};""").fetchall()
            for i in g:
                s = f'Тренировка номер {i[0]}, информация о тренировке: {i[1]}, дата тренировки: {i[3]}'
            btn1 = types.KeyboardButton("Записаться на тренировку")
            btn2 = types.KeyboardButton("Отписаться от тренировки")
            btn3 = types.KeyboardButton("+1")
            btn4 = types.KeyboardButton("-1")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, btn3, btn4, back)
            bot.send_message(message.chat.id, text=s, reply_markup=markup)
        except:
            bot.send_message(message.chat.id, text='Вы ввели не корректное число, попробуйте снова.')
            game_check = 5
    elif message.text == 'Записаться на тренировку':
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        s = []
        k = ''
        for i in g:
            s.append(i[0].split(', '))
        s = s[0]
        if name not in s:
            s.append(name)
            k = ', '.join(s)
            cur.execute(f"""UPDATE first SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
            con.commit()
        else:
            bot.send_message(message.chat.id, text='Вы уже записаны.')
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        k = g[0][0].replace(', ', '\n')
        k = k + '\n' + f'{k.count(f"{n}")} человек записано'
        bot.send_message(message.chat.id, text=k)

    elif message.text == 'Отписаться от тренировки':
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        s = []
        k = ''
        for i in g:
            s.append(i[0].split(', '))
        s = s[0]
        if name in s:
            del s[s.index(name)]
            k = ', '.join(s)
            cur.execute(f"""UPDATE first SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
            con.commit()
        else:
            bot.send_message(message.chat.id, text='Вы еще не записаны.')
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        k = g[0][0].replace(', ', '\n')
        k = k + '\n' + f'{k.count(f"{n}") + 1} человек записано'
        bot.send_message(message.chat.id, text=k)
    elif message.text == '+1':
        name = f'+1'
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        s = []
        k = ''
        for i in g:
            s.append(i[0].split(', '))
        s = s[0]
        s.append(name)
        k = ', '.join(s)
        cur.execute(f"""UPDATE first SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
        con.commit()
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        k = g[0][0].replace(', ', '\n')
        k = k + '\n' + f'{k.count(f"{n}")} человек записано'
        bot.send_message(message.chat.id, text=k)

    elif message.text == '-1':
        name = f'+1'
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        s = []
        k = ''
        for i in g:
            s.append(i[0].split(', '))
        s = s[0]
        if name in s:
            del s[s.index(name)]
            k = ', '.join(s)
            cur.execute(f"""UPDATE first SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
            con.commit()
        else:
            bot.send_message(message.chat.id, text='Вы еще не записаны.')
        g = cur.execute(f"""SELECT names FROM first WHERE id = {prac_numb};""").fetchall()
        k = g[0][0].replace(', ', '\n')
        k = k + '\n' + f'{k.count(f"{n}")} человек записано'
        bot.send_message(message.chat.id, text=k)

    elif game_check == 6:
        s = ''
        status = ['creator', 'administrator']
        game_check = 0
        prac_numb = int(message.text)
        g = cur.execute(f"""SELECT * FROM game WHERE id = {prac_numb};""").fetchall()
        user_status = str(bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id).status)
        if user_status in status:
            for i in g:
                s = f'Игра номер {i[0]},{n} информация о игре: {i[1]},{n} дата игры: {i[3]}'
            btn1 = types.KeyboardButton("Записаться на игру")
            btn2 = types.KeyboardButton("Отписаться от игры")
            btn3 = types.KeyboardButton("++1")
            btn4 = types.KeyboardButton("--1")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, btn3, btn4, back)
            bot.send_message(message.chat.id, text=s, reply_markup=markup)
        else:
            for i in g:
                s = f'Игра номер {i[0]},{n} информация о игре: {i[1]},{n} дата игры: {i[3]}'
            btn1 = types.KeyboardButton("Записаться на игру")
            btn2 = types.KeyboardButton("Отписаться от игры")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text=s, reply_markup=markup)
    elif message.text == 'Записаться на игру':
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
        g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
        s = []
        k = ''
        for i in g:
            s.append(i[0].split(', '))
        s = s[0]
        if name not in s:
            s.append(name)
            k = ', '.join(s)
            cur.execute(f"""UPDATE game SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
            con.commit()
        else:
            bot.send_message(message.chat.id, text='Вы уже записаны.')
        g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
        k = g[0][0].replace(', ', '\n')
        k = k + '\n' + f'{k.count(f"{n}")} человек записано'
        bot.send_message(message.chat.id, text=k)

    elif message.text == 'Отписаться от игры':
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
        g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
        s = []
        k = ''
        for i in g:
            s.append(i[0].split(', '))
        s = s[0]
        if name in s:
            del s[s.index(name)]
            k = ', '.join(s)
            cur.execute(f"""UPDATE game SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
            con.commit()
        else:
            bot.send_message(message.chat.id, text='Вы еще не записаны.')
        g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
        k = g[0][0].replace(', ', '\n')
        k = k + '\n' + f'{k.count(f"{n}")} человек записано'
        bot.send_message(message.chat.id, text=k)

    elif message.text == '++1':
        status = ['creator', 'administrator']
        user_status = str(bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id).status)
        if user_status in status:
            name = f'+1'
            g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
            s = []
            k = ''
            for i in g:
                s.append(i[0].split(', '))
            s = s[0]
            s.append(name)
            k = ', '.join(s)
            cur.execute(f"""UPDATE game SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
            con.commit()
            g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
            k = g[0][0].replace(', ', '\n')
            k = k + '\n' + f'{k.count(f"{n}")} человек записано'
            bot.send_message(message.chat.id, text=k)
        else:
            bot.send_message(message.chat.id, text='У вас нет прав для этой команды.')

    elif message.text == '--1':
        status = ['creator', 'administrator']
        user_status = str(bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id).status)
        if user_status in status:
            name = f'+1'
            g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
            s = []
            k = ''
            for i in g:
                s.append(i[0].split(', '))
            s = s[0]
            if name in s:
                del s[s.index(name)]
                k = ', '.join(s)
                cur.execute(f"""UPDATE game SET names = '{k}' WHERE id = {prac_numb}""").fetchall()
                con.commit()
            else:
                bot.send_message(message.chat.id, text='Вы еще не записаны.')
            g = cur.execute(f"""SELECT names FROM game WHERE id = {prac_numb};""").fetchall()
            k = g[0][0].replace(', ', '\n')
            k = k + '\n' + f'{k.count(f"{n}")} человек записано'
            bot.send_message(message.chat.id, text=k)
        else:
            bot.send_message(message.chat.id, text='У вас нет прав для этой команды.')


bot.polling(none_stop=True)
