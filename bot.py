import telebot
import re
import youtube_dl
import os
bot = telebot.TeleBot("***REMOVED***")
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@bot.message_handler(commands=['start'])
def start_message(message):
    
    #LOG START
    print(bcolors.FAIL + 'BOT STARTED\n' +
    bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(message.chat.id) + '\n'
    + bcolors.ENDC)
    #LOG END
    
    bot.reply_to(message, "Hi!! Welcome to the YTDL Bot made by @galisteo02!!")

@bot.message_handler(commands=['help'])
def help_message(message):

    #LOG START
    print(bcolors.FAIL + 'HELP REQUESTED\n' +
    bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(message.chat.id) + '\n'
    + bcolors.ENDC)
    #LOG END

    bot.reply_to(message,
	'/start: Display a welcome message and credits\n'+
	'/help: Display all commands available with descriptions\n' +
	'/dl: Download a video [/dl URL]\n' +
    '/dlmp3: Download a video on mp3 [/dlmp3 URL]\n' + 
    '/id: Get the video ID [/id URL]'
	)

@bot.message_handler(commands=['dl'], content_types=['text'])
def dl(message):
    bot.send_message(message.chat.id, 'On the way!')
    url = re.findall(r'(https?://\S+)', message.text)
    video_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text)

    #LOG START
    print(bcolors.WARNING + 'REQUEST FOR MP4 DOWNLOAD CREATED\n' +
    bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(message.chat.id) + '\n' +
    bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url[-1] + '\n' +
    bcolors.OKGREEN + 'Video ID: ' + bcolors.OKCYAN + video_id[-1] + bcolors.ENDC)
    #LOG END

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

@bot.message_handler(commands=['dlmp3'], content_types=['text'])
def dlmp3(message):
    bot.send_message(message.chat.id, 'On the way!')
    url = re.findall(r'(https?://\S+)', message.text)
    audio_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text)
    
    #LOG START
    print(bcolors.WARNING + 'REQUEST FOR MP3 DOWNLOAD CREATED\n' +
    bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(message.chat.id) + '\n' +
    bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url[-1] + '\n' +
    bcolors.OKGREEN + 'Audio ID: ' + bcolors.OKCYAN + audio_id[-1] + bcolors.ENDC)
    #LOG END

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

@bot.message_handler(commands=['id'], content_types=['text'])
def send_video_id(message):
    url = re.findall(r'(https?://\S+)', message.text)
    video_id = re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]+)", message.text)

    #LOG START
    print(bcolors.WARNING + 'REQUEST FOR ID CREATED\n' +
    bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(message.chat.id) + '\n' +
    bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url[-1] + '\n' +
    bcolors.OKGREEN + 'ID: ' + bcolors.OKCYAN + video_id[-1] + bcolors.ENDC)
    #LOG END

    bot.reply_to(message, 'Video ID: ' + video_id[-1])

bot.polling()