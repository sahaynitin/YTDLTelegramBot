import telebot
import re
import youtube_dl
import os
bot = telebot.TeleBot("***REMOVED***")

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.reply_to(message, "Hi!! Welcome to the Downloader Bot made by @galisteo02!!")
	
@bot.message_handler(commands=['help'])
def help_message(message):
	bot.reply_to(message,
	'/help: Display all commands available\n' +
	'/start: Display a greetings message and the creators @ \n' +
	'/dl: Download a video [/dl url]'
    '/id: Get the video ID'
	)

@bot.message_handler(commands=['dl'], content_types=['text'])
def dl(message):
    bot.send_message(***REMOVED***, 'On the way!')
    url = re.findall(r'(https?://\S+)', message.text)
    video_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text)
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    bot.send_message(***REMOVED***, 'Downloading... (This could take a while)')
    with ydl:
        ydl.download(url)
    bot.send_message(***REMOVED***, 'Sending video...')
    video = open(video_id[-1] + '.mp4', 'rb')
    bot.send_video(***REMOVED***, video)
    os.remove(video_id[-1] + '.mp4')
    bot.send_message(***REMOVED***, 'Done!')

@bot.message_handler(commands=['id'], content_types=['text'])
def send_video_id(message):
    url = re.findall(r'(https?://\S+)', message.text)
    video_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text)
    bot.reply_to(message, 'Video ID: ' + video_id[-1])

bot.polling()