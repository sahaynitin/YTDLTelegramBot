import youtube_dl
import os
import telebot
from Extra.messages import print_log, print_log_simple, progress_msg
bot = telebot.TeleBot("***REMOVED***") #OG BOT
#bot = telebot.TeleBot("***REMOVED***") #TEST BOT

# cid: Content ID
# url: Content URL

def is_supported(url): #CHECK IS URL IS SUPPORTED
    if 'vm.tiktok.com' in url:
        return True
    else:
        ies = youtube_dl.extractor.gen_extractors()
        for ie in ies:
            if ie.suitable(url) and ie.IE_NAME != 'generic':
                return True
        return False

def getfilename(cid):
    if os.path.isfile(cid+'.mkv'):
        extension = '.mkv'
        filename= cid+extension
        return filename
    elif os.path.isfile(cid+'.mp4'):
        extension = '.mp4'
        filename= cid+extension
        return filename
    elif os.path.isfile(cid+'.webm'):
        extension = '.webm'
        filename= cid+extension
        return filename
    elif os.path.isfile(cid+'.mp3'):
        extension = '.mp3'
        filename= cid+extension
        return filename

def download(typem, sts, chatid, cid, url, message):

    print_log(typem, sts, chatid, cid, url, message)
    progress_msg(chatid, 1, typem)
    if typem == 'dl':
        ydl_opts = {
        'outtmpl': cid[-1] + '.%(ext)s',
        }
    if typem == 'dlmp3':
        ydl_opts = {
        'outtmpl': cid[-1] + '.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    progress_msg(chatid, 2, typem)
    try:
        with ydl:
            ydl.download(url)
    except youtube_dl.utils.DownloadError:
        print_log(typem, 'D_ERROR', chatid, cid, url, message)
        return
    progress_msg(chatid, 3, typem)
    filename = getfilename(cid[-1])
    file = open(filename, 'rb')
    if typem == 'dl':
        bot.send_video(chatid, file)
    if typem == 'dlmp3':
        bot.send_audio(chatid, file)
    os.remove(filename)
    progress_msg(chatid, 4, typem)
