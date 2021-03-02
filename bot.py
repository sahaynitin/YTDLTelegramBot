import telebot
import re
import os
from Extra.classes import bcolors, replies
from Extra.functions import is_supported, download
from Extra.messages import print_log, print_log_simple

token = os.environ['TELEGRAM_TOKEN'] #GET TOKEN FROM HEROKU
bot = telebot.TeleBot(token) # OG BOT
#bot = telebot.TeleBot("***REMOVED***") #TEST BOT

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'help':
        help_message(call.message)

@bot.message_handler(commands=['start']) #CHECK FOR /START
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Help ℹ️', callback_data='help'))
    print_log_simple('start', message.chat.id)
    bot.send_message(message.chat.id, replies.WELCOME, reply_markup=markup)

@bot.message_handler(commands=['help']) #CHECK FOR /HELP
def help_message(message):
    print_log_simple('help', message.chat.id)
    bot.send_message(message.chat.id, replies.HELP)

@bot.message_handler(commands=['dl'], content_types=['text']) #CHECK FOR /dl
def dl(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    cid = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET CONTENT ID

    if url: #CHECK IF URL EXIST AND URL IS SUPPORTED
        if is_supported(url[-1]): #CHECK IF URL IS SUPPORTED
            download('video', 'OK', message.chat.id, cid, url, message, bot)
        else:
            print_log('video', 'SUPP_ERROR', message.chat.id, cid, url, message, bot)
    else:
        print_log('video', 'URL_ERROR', message.chat.id, cid, url, message, bot)

@bot.message_handler(commands=['dlmp3'], content_types=['text']) #CHECK FOR /dlmp3
def dlmp3(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    cid = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET CONTENT ID

    if url: #CHECK IF URL EXIST
        if is_supported(url[-1]): #CHECK IF URL IS SUPPORTED
            download('audio', 'OK', message.chat.id, cid, url, message, bot)
        else:
            print_log('audio', 'SUPP_ERROR', message.chat.id, cid, url, message, bot)
    else:
        print_log('audio', 'URL_ERROR', message.chat.id, cid, url, message, bot)

@bot.message_handler(commands=['id'], content_types=['text']) #CHECK FOR /id
def send_video_id(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    cid = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET CONTENT ID

    if url:
        if is_supported(url[-1]):
            print_log('id', 'OK', message.chat.id, cid, url, message, bot)
            bot.send_message(message.chat.id, replies.DISCLAIMER)
            bot.send_message(message.chat.id, replies.ID + cid[-1])
        else:
            print_log('id', 'SUPP_ERROR', message.chat.id, cid, url, message, bot)
    else:
        print_log('id', 'URL_ERROR', message.chat.id, cid, url, message, bot)

bot.polling()
