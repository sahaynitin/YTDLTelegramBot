import telebot
import re
import youtube_dl
import os
from Extra.classes import bcolors
from Extra.functions import is_supported
from Extra.messages import print_log, print_log_simple, progress_msg
bot = telebot.TeleBot("***REMOVED***") # OG BOT
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
    bot.send_message(message.chat.id, 'Hi!! 👋\n' +
                                      'Welcome to the YTDL Bot made by @galisteo02!!',
                                       reply_markup=markup)

@bot.message_handler(commands=['help']) #CHECK FOR /HELP
def help_message(message):
    print_log_simple('help', message.chat.id)
    bot.send_message(message.chat.id,
	'/start: Display a welcome message and credits\n'+
	'/help: Display all commands available with descriptions\n' +
	'/dl: Download a video [/dl URL]\n' +
    '/dlmp3: Download a video on mp3 [/dlmp3 URL]\n' +
    '/id: Get the video ID [/id URL]'
	)

@bot.message_handler(commands=['dl'], content_types=['text']) #CHECK FOR /dl
def dl(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    video_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET VIDEO ID

    if url and is_supported(url[-1]): #CHECK IF URL EXIST AND URL IS SUPPORTED
        print_log('dl', 'OK', message.chat.id, video_id, url, message)
        progress_msg(message.chat.id, 1)
        ydl_opts = {'outtmpl': video_id[-1] + '.%(ext)s'}
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        progress_msg(message.chat.id, 2)
        try:
            with ydl:
                ydl.download(url)
        except youtube_dl.utils.DownloadError:
            print_log('dl', 'D_ERROR', message.chat.id, audio_id, url, message)
            return
        progress_msg(message.chat.id, 3)
        video = open(video_id[-1] + '.mp4', 'rb')
        bot.send_video(message.chat.id, video)
        os.remove(video_id[-1] + '.mp4')
        progress_msg(message.chat.id, 4)
    else:
        print_log('dl', 'ERROR', message.chat.id, video_id, url, message)

@bot.message_handler(commands=['dlmp3'], content_types=['text']) #CHECK FOR /dlmp3
def dlmp3(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    audio_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET AUDIO ID

    if url and is_supported(url[-1]): #CHECK IF URL EXIST AND URL IS SUPPORTED
        print_log('dlmp3', 'OK', message.chat.id, audio_id, url, message)
        progress_msg(message.chat.id, 1)
        ydl_opts = {
            'outtmpl': audio_id[-1] + '.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],}
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        progress_msg(message.chat.id, 2)
        try:
            with ydl:
                ydl.download(url)
        except youtube_dl.utils.DownloadError:
            print_log('dlmp3', 'D_ERROR', message.chat.id, audio_id, url, message)
            return
        progress_msg(message.chat.id, 3)
        audio = open(audio_id[-1] + '.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
        os.remove(audio_id[-1] + '.mp3')
        progress_msg(message.chat.id, 4)

    else:
        print_log('dlmp3', 'ERROR', message.chat.id, audio_id, url, message)

@bot.message_handler(commands=['id'], content_types=['text']) #CHECK FOR /id
def send_video_id(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    video_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET VIDEO ID

    if url and is_supported(url[-1]):
        print_log('id', 'OK', message.chat.id, video_id, url, message)
        bot.send_message(message.chat.id, '⚠️ DISCLAIMER ⚠️\n'+ '\n' + '🆔 not always corresponds to the real one!!')
        bot.send_message(message.chat.id, '🆔 ==> ' + video_id[-1])
    else:
        print_log('id', 'ERROR', message.chat.id, video_id, url, message)

bot.polling()
