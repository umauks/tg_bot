import json

import telebot
from telebot import types

from game import *

bot = telebot.TeleBot('6668403270:AAFeP3DBQJTxXtQ2RqEs-D6fQR_ZJAjx7IU')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет! Чтобы запустить квест пропиши команду /start_quest")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start - запуск бота\n/help - помощь\n/start_quest - "
                                      "запуск квеста")

def location_game(chat_id, location):
    if 'media' in location:
        bot.send_photo(chat_id, open(location['media'], 'rb'))
    bot.send_message(chat_id, location['description'])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for actions in location['actions']:
        button = types.KeyboardButton(actions)
        markup.add(button)
    bot.send_message(chat_id, "Выбирай⬇️⬇️⬇️", reply_markup=markup)

@bot.message_handler(commands=['start_quest'])
def start_quest(message):
    with open('locations.json', 'r', encoding='utf-8') as f:
        locations = json.load(f)
        start_loc = locations['start']
    location_game(message.chat.id, start_loc)
    save_progress(message.chat.id, 'start')

@bot.message_handler(func=lambda message: True)
def choice(message):
    user_choice = message.text
    try:
        with open('locations.json', 'r', encoding='utf-8') as f:
            locations = json.load(f)
        current_location_key = load_progress(message.chat.id)
        current_location = locations[current_location_key]

        if message.text in current_location['actions']:
            next_location_key = current_location['actions'][user_choice]
            next_location = locations[next_location_key]
            location_game(message.chat.id, next_location)
            save_progress(message.chat.id, next_location_key)

        elif message.text not in current_location['actions']:
            bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")

    except Exception:
        bot.send_message(message.chat.id,'Произошла ошибка, чтобы пройти квест, напишите /start_quest')


bot.polling()