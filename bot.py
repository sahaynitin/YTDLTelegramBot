import telebot
import re
import os
from Extra.classes import replies
from Extra.functions import is_supported, download
from Extra.messages import print_log, print_log_simple, print_except

token = os.environ['TELEGRAM_TOKEN'] #GET TOKEN FROM ENVIRONMENT
bot = telebot.TeleBot(token)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'help':
        try:
            bot.edit_message_text(replies.WELCOME + '\n' + '\n' + 'HELP ⬇️', chat_id=msgcid, message_id= msgid)
            help_message(call.message)
        except:
            fail(call.message)
    if call.data == 'errors':
        try:
            bot.edit_message_text(replies.WELCOME + '\n' + '\n' + 'ERRORS INFO ⬇️', chat_id=msgcid, message_id= msgid)
            errors_info(call.message)
        except:
            fail(call.message)
    if call.data == 'dl':
        try:
            bot.edit_message_text(text= '<b>URL: </b>' + '' + url + '<b>\nSelect Download Option:</b> MP4', chat_id= msgcid, message_id= msgid, disable_web_page_preview=True, parse_mode='HTML')
            bot.answer_callback_query(call.id, text='MP4 Download Selected')
            dl(call.message)
        except:
            fail(call.message)
    if call.data == 'dlmp3':
        try:
            bot.edit_message_text(text= '<b>URL: </b>' + '' + url + '<b>\nSelected Download Option:</b> MP3', chat_id= msgcid, message_id= msgid, disable_web_page_preview=True, parse_mode='HTML')
            bot.answer_callback_query(call.id, text='MP3 Download Selected')
            dlmp3(call.message)
        except:
            fail(call.message)
    if call.data == 'howto':
        try:
            bot.edit_message_text(replies.WELCOME + '\n' + '\n' + 'HOW TO DOWNLOAD ⬇️', chat_id=msgcid, message_id= msgid)
            how_to_message(call.message)
        except:
            fail(call.message)
    if call.data == 'canceldl':
        try:
            bot.edit_message_text(text= '<b>URL: </b>' + '' + url + '\n\nCANCELED DOWNLOAD 😔', chat_id= msgcid, message_id= msgid, disable_web_page_preview=True, parse_mode='HTML')
        except:
            fail(call.message)

@bot.message_handler(commands=['dl', 'dlmp3']) #CHECK FOR /errors
def new_way(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='ℹ️ How to download ℹ️', callback_data='howto'))
    bot.reply_to(message, replies.NEW_WAY, reply_markup=markup)

@bot.message_handler(commands=['start']) #CHECK FOR /start
def start_message(message):
    global url
    global msgid
    global msgcid
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='ℹ️ How to download ℹ️', callback_data='howto'))
    markup.add(telebot.types.InlineKeyboardButton(text='ℹ️ Help ℹ️', callback_data='help'))
    markup.add(telebot.types.InlineKeyboardButton(text='🚨 Errors Info 🚨', callback_data='errors'))
    print_log_simple('start', message.chat.id)
    msg = bot.send_message(message.chat.id, replies.WELCOME, reply_markup=markup)
    msgid = msg.message_id
    msgcid = msg.chat.id

@bot.message_handler(commands=['help']) #CHECK FOR /help
def help_message(message):
    print_log_simple('help', message.chat.id)
    bot.send_message(message.chat.id, replies.HELP)

@bot.message_handler(commands=['howto'])
def how_to_message(message):
    bot.send_message(message.chat.id, replies.HOW_TO)

@bot.message_handler(commands=['errors']) #CHECK FOR /errors
def errors_info(message):
    print_log_simple('errors', message.chat.id)
    bot.send_message(message.chat.id, replies.ERRORS)

@bot.message_handler(regexp=(r'(https?://\S+)'))
def function_name(message):
    try:
        global url
        global msgid
        global msgcid
        global cid
        cid = message.chat.id
        url = re.search("(?P<url>https?://[^\s'\"]+)", message.text).group("url")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton(text='MP4 📹', callback_data='dl'),
            telebot.types.InlineKeyboardButton(text='MP3 🎵', callback_data='dlmp3'),
        )
        markup.add(telebot.types.InlineKeyboardButton(text='CANCEL DOWNLOAD 🛑', callback_data='canceldl'))
        msg = bot.send_message(message.chat.id, '<b>URL: </b>' + '' + url + '<b>\nSelect Download Option</b> ⬇️', reply_markup=markup, disable_web_page_preview=True, parse_mode='HTML')
        msgid = msg.message_id
        msgcid = msg.chat.id
    except Exception as exception:
        print_except(exception, message.chat.id, url, bot)

@bot.message_handler(regexp="")
def no_url(message):
    print_log('URL', 'URL_ERROR', message.chat.id, 'NO_URL', message, bot)

@bot.message_handler()
def fail(message):
    bot.send_message(message.chat.id, 'Failed to retrieve message from past session 🚨')

def dl(message):
    try:
        url = message.text.split()[1]
        if is_supported(url, message.chat.id, bot): #CHECK IF URL IS SUPPORTED
            lurl = re.findall(r'(https?://\S+)', url)
            download('video', 'OK', message.chat.id, url, message, bot, lurl)
        else:
            print_log('video', 'SUPP_ERROR', message.chat.id, url, message, bot)
    except Exception as exception:
        print_except(exception, message.chat.id, url, bot)

def dlmp3(message):
    try:
        url = message.text.split()[1]
        if is_supported(url, message.chat.id, bot): #CHECK IF URL IS SUPPORTED
            lurl = re.findall(r'(https?://\S+)', url)
            download('audio', 'OK', message.chat.id, url, message, bot, lurl)
        else:
            print_log('audio', 'SUPP_ERROR', message.chat.id, url, message, bot)
    except Exception as exception:
        print_except(exception, message.chat.id, url, bot)

bot.polling()
