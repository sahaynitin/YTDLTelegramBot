import youtube_dl
import os
import telebot
from Extra.messages import print_log, print_log_simple, progress_msg, print_except
from Extra.classes import replies

# date: date
# url: Content URL [str]
# lurl: Content URL [list]
# typem: Type Of Petition [MP3, MP4, ID]
# case: ERROR or OK
# chatid: ID of the chat [message.chat.id]
# bot: API Token from Telebot
# case: STATUS [OK or TYPE_ERROR]
# message: message handler for reply_to

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

def getfilename(date, chatid, url, bot):
    try:
        if os.path.isfile(date+'_'+str(chatid)+'.mkv'):
            extension = '.mkv'
            filename= date+'_'+str(chatid)+extension
            return filename
        elif os.path.isfile(date+'_'+str(chatid)+'.mp4'):
            extension = '.mp4'
            filename= date+'_'+str(chatid)+extension
            return filename
        elif os.path.isfile(date+'_'+str(chatid)+'.webm'):
            extension = '.webm'
            filename= date+'_'+str(chatid)+extension
            return filename
        elif os.path.isfile(date+'_'+str(chatid)+'.mp3'):
            extension = '.mp3'
            filename= date+'_'+str(chatid)+extension
            return filename
    except Exception as error:
            print_except(error, chatid, url, bot)

def download(typem, case, chatid, date, url, message, bot, lurl):
    try:
        print_log(typem, case, chatid, url, message, bot)
        progress_msg(chatid, 1, typem, bot)
        if typem == 'video':
            ydl_opts = {'outtmpl': date + '_' + str(chatid) + '.%(ext)s'}
        if typem == 'audio':
            ydl_opts = {
            'outtmpl': date + '_' + str(chatid) + '.%(ext)s',
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
                ydl.download(lurl)
        except youtube_dl.utils.DownloadError:
            print_log(typem, 'D_ERROR', chatid, url, message, bot)
            return
        progress_msg(chatid, 3, typem, bot)
        filename = getfilename(date, chatid, url, bot)
        file = open(filename, 'rb')
        if typem == 'video':
            bot.send_video(chatid, file)
        if typem == 'audio':
            bot.send_audio(chatid, file)
        os.remove(filename)
        progress_msg(chatid, 4, typem, bot)
    except:
        try:
            if typem == 'video':
                bot.send_message(chatid, replies.FILE_TOO_BIG)
                os.remove(filename)
                get_link(url, message, bot, chatid, typem)
        except Exception as error:
            if filename:
                os.remove(filename)
            print_except(error, chatid, url, bot)

def get_link(url, message, bot, chatid, typem):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    try:
        with ydl:
            result = ydl.extract_info(url, download=False) # We just want to extract the info
        if 'entries' in result: # Can be a playlist or a list of videos
            video = result['entries'][0]
        else: # Just a video
            video = result
        a = -1
        for i in video['formats']:
            a = a + 1
        link = '<a href=\"' + video['formats'][a]['url'] + '\">' + video['formats'][a]['format_note'] + '</a>'
        bot.reply_to(message, 'Quality ' + link, parse_mode='HTML')
        progress_msg(chatid, 4, typem, bot)
    except Exception as error:
        print_except(error, chatid, url, bot)
