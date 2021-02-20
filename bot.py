import telebot
import re
import youtube_dl
import os
from Extra.classes import bcolors
from Extra.checks import is_supported
from Extra.messages import print_log, print_log_simple
#bot = telebot.TeleBot("***REMOVED***") #OG BOT
bot = telebot.TeleBot("***REMOVED***") #TEST BOT

@bot.message_handler(commands=['start']) #CHECK FOR /START
def start_message(message):
    
    print_log_simple('start', message.chat.id)
    
    bot.reply_to(message, "Hi!! Welcome to the YTDL Bot made by @galisteo02!!")

@bot.message_handler(commands=['help']) #CHECK FOR /HELP
def help_message(message):

    print_log_simple('help', message.chat.id)

    bot.reply_to(message,
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

        bot.send_message(message.chat.id, 'On the way!')

        ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        bot.send_message(message.chat.id, 'Downloading... (This could take a while)')
        with ydl:
            ydl.download(url)
        
        bot.send_message(message.chat.id, 'Sending video...')

        video = open(video_id[-1] + '.mp4', 'rb')
        bot.send_video(message.chat.id, video)
        os.remove(video_id[-1] + '.mp4')

        bot.send_message(message.chat.id, 'Done!')
    else:
        print_log('dl', 'ERROR', message.chat.id, video_id, url, message)

@bot.message_handler(commands=['dlmp3'], content_types=['text']) #CHECK FOR /dlmp3
def dlmp3(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    audio_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET AUDIO ID

    if url and is_supported(url[-1]): #CHECK IF URL EXIST AND URL IS SUPPORTED
        print_log('dlmp3', 'OK', message.chat.id, audio_id, url, message)

        bot.send_message(message.chat.id, 'On the way!')

        ydl_opts = {
            'outtmpl': '%(id)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
            }
        ydl = youtube_dl.YoutubeDL(ydl_opts)

        bot.send_message(message.chat.id, 'Downloading... (This could take a while)')

        with ydl:
            ydl.download(url)
        
        bot.send_message(message.chat.id, 'Sending audio...')

        audio = open(audio_id[-1] + '.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
        os.remove(audio_id[-1] + '.mp3')

        bot.send_message(message.chat.id, 'Done!')
    
    else:
        print_log('dlmp3', 'ERROR', message.chat.id, audio_id, url, message)

@bot.message_handler(commands=['id'], content_types=['text']) #CHECK FOR /id
def send_video_id(message):
    url = re.findall(r'(https?://\S+)', message.text) #PARSE URL
    video_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text) #GET VIDEO ID
    
    if url and is_supported(url[-1]):
        print_log('id', 'OK', message.chat.id, video_id, url, message)

        bot.reply_to(message, 'Video ID: ' + video_id[-1])
    else:
        print_log('id', 'ERROR', message.chat.id, video_id, url, message)

bot.polling()