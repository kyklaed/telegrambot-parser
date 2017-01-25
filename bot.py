# -*- coding: utf-8 -*-

"""
Бот выдающий случайный рецепт из базы.
"""

import telebot
import baza

bot = telebot.TeleBot("")


@bot.message_handler(commands = ["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.InlineKeyboardButton(text = "Бульоны и супы!")
    btn2 = telebot.types.InlineKeyboardButton(text = "Горячие блюда!")
    btn3 = telebot.types.InlineKeyboardButton(text="Салат!")
    btn4 = telebot.types.InlineKeyboardButton(text="Закуски!")
    btn5 = telebot.types.InlineKeyboardButton(text="Напитки!")
    btn6 = telebot.types.InlineKeyboardButton(text="Соусы!")
    btn7 = telebot.types.InlineKeyboardButton(text="Выпечка!")
    btn8 = telebot.types.InlineKeyboardButton(text="Десерты!")
    btn9 = telebot.types.InlineKeyboardButton(text="Каши!")
    keyboard.add(btn1, btn2, btn3)
    keyboard.add(btn4, btn5, btn6)
    keyboard.add(btn7, btn8, btn9)
    
    bot.send_message(message.from_user.id,"Привет, что бы получить случайный рецепт нажмите на кнопку под диалогом! ", reply_markup = keyboard)

@bot.message_handler(command = ["help"])
def help_prog (message):
    bot.send_message (message.chat.id,"help в разработке")

@bot.message_handler(commands = ["brothsoups"])
def brothsoups(message):
    db = baza.Basesql('cooking.db','brothsoups')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["hotmeals"])
def hotmeals(message):
    db = baza.Basesql('cooking.db','hotmeals')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["salad"])
def salad(message):
    db = baza.Basesql('cooking.db','salad')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["snacks"])
def snacks(message):
    db = baza.Basesql('cooking.db','snacks')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["drinks"])
def drinks(message):
    db = baza.Basesql('cooking.db','drinks')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["sauces"])
def sauces(message):
    db = baza.Basesql('cooking.db','sauces')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["cakes"])
def cakes(message):
    db = baza.Basesql('cooking.db','cakes')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["desserts"])
def desserts(message):
    db = baza.Basesql('cooking.db','desserts')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

@bot.message_handler(commands = ["porridge"])
def porridge(message):
    db = baza.Basesql('cooking.db','porridge')
    id, recip = db.select_random()
    bot.send_message(message.chat.id, '{0}' .format(recip))

var = {"Бульоны и супы!": brothsoups, "Горячие блюда!": hotmeals,
       "Салат!": salad,"Закуски!":snacks,"Напитки!":drinks,"Соусы!":sauces,"Выпечка!":cakes,
       "Десерты!":desserts,"Каши!":porridge}
@bot.message_handler(content_types = ["text"])
def variant(message):
    
    if message.text not in var.keys(): 
        bot.send_message(message.chat.id, 'Нажмите кнопку под окном диалога, если кнопок нет то введите команду /start')
    else:
        var[message.text](message)


bot.polling(none_stop=True)

