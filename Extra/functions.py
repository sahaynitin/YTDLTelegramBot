import youtube_dl
import os
import telebot
from Extra.messages import print_log, print_log_simple, progress_msg, print_except

# cid: Content ID
# url: Content URL

def is_supported(url, chatid, bot): #CHECK IS URL IS SUPPORTED
    try:
        if 'vm.tiktok.com' in url:
            return True
        else:
            ies = youtube_dl.extractor.gen_extractors()
            for ie in ies:
                if ie.suitable(url) and ie.IE_NAME != 'generic':
                    return True
            return False
    except Exception as error:
            print_except(error, chatid, url, bot)

def getfilename(cid, chatid, url, bot):
    try:
        if os.path.isfile(cid+'_'+str(chatid)+'.mkv'):
            extension = '.mkv'
            filename= cid+'_'+str(chatid)+extension
            return filename
        elif os.path.isfile(cid+'_'+str(chatid)+'.mp4'):
            extension = '.mp4'
            filename= cid+'_'+str(chatid)+extension
            return filename
        elif os.path.isfile(cid+'_'+str(chatid)+'.webm'):
            extension = '.webm'
            filename= cid+'_'+str(chatid)+extension
            return filename
        elif os.path.isfile(cid+'_'+str(chatid)+'.mp3'):
            extension = '.mp3'
            filename= cid+'_'+str(chatid)+extension
            return filename
    except Exception as error:
            print_except(error, chatid, url, bot)

def download(typem, sts, chatid, cid, url, message, bot):
    try:
        print_log(typem, sts, chatid, cid, url, message, bot)
        progress_msg(chatid, 1, typem, bot)
        if typem == 'video':
            ydl_opts = {
            'outtmpl': cid[-1] + '_' + str(chatid) + '.%(ext)s',
            }
        if typem == 'audio':
            ydl_opts = {
            'outtmpl': cid[-1] + '_' + str(chatid) + '.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],}
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        progress_msg(chatid, 2, typem, bot)
        try:
            with ydl:
                ydl.download(url)
        except youtube_dl.utils.DownloadError:
            print_log(typem, 'D_ERROR', chatid, cid, url, message, bot)
            return
        progress_msg(chatid, 3, typem, bot)
        filename = getfilename(cid[-1], chatid, url, bot)
        file = open(filename, 'rb')
        if typem == 'video':
            bot.send_video(chatid, file)
        if typem == 'audio':
            bot.send_audio(chatid, file)
        os.remove(filename)
        progress_msg(chatid, 4, typem, bot)
    except Exception as error:
            print_except(error, chatid, url, bot)
