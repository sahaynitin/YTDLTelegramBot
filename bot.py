import telebot
import re
import os
from datetime import datetime
from Extra.classes import bcolors, replies
from Extra.functions import is_supported, download, get_link
from Extra.messages import print_log, print_log_simple

token = os.environ['TELEGRAM_TOKEN'] #GET TOKEN FROM HEROKU
bot = telebot.TeleBot(token) # OG BOT
#bot = telebot.TeleBot("***REMOVED***") #TEST BOT

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'help':
        help_message(call.message)
    if call.data == 'errors':
        errors_info(call.message)

@bot.message_handler(commands=['start']) #CHECK FOR /start
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='ℹ️ Help ℹ️', callback_data='help'))
    markup.add(telebot.types.InlineKeyboardButton(text='🚨 Errors Info 🚨', callback_data='errors'))
    print_log_simple('start', message.chat.id)
    bot.send_message(message.chat.id, replies.WELCOME, reply_markup=markup)

@bot.message_handler(commands=['help']) #CHECK FOR /help
def help_message(message):
    print_log_simple('help', message.chat.id)
    bot.reply_to(message, replies.HELP)

@bot.message_handler(commands=['errors']) #CHECK FOR /errors
def errors_info(message):
    print_log_simple('errors', message.chat.id)
    bot.reply_to(message, replies.ERRORS)

@bot.message_handler(commands=['dl']) #CHECK FOR /dl
def dl(message):
    now = datetime.now()
    date = now.strftime("%d%m%Y" + "%H%M%S")
    chatid = message.chat.id

    try:
        url = message.text.split()[1]
        if is_supported(url, chatid, bot): #CHECK IF URL IS SUPPORTED
            lurl = re.findall(r'(https?://\S+)', url)
            download('video', 'OK', chatid, date, url, message, bot, lurl)
        else:
            print_log('video', 'SUPP_ERROR', chatid, url, message, bot)
    except:
        print_log('video', 'URL_ERROR', chatid, 'NO_URL', message, bot)

@bot.message_handler(commands=['dlmp3']) #CHECK FOR /dlmp3
def dlmp3(message):
    now = datetime.now()
    date = now.strftime("%d%m%Y" + "%H%M%S")
    chatid = message.chat.id

    try:
        url = message.text.split()[1]
        if is_supported(url, chatid, bot): #CHECK IF URL IS SUPPORTED
            lurl = re.findall(r'(https?://\S+)', url)
            download('audio', 'OK', chatid, date, url, message, bot, lurl)
        else:
            print_log('audio', 'SUPP_ERROR', chatid, url, message, bot)
    except:
        print_log('audio', 'URL_ERROR', chatid, 'NO_URL', message, bot)

bot.polling()
