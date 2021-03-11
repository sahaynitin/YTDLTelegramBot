import youtube_dl
import pafy
import os
import time
from Extra.messages import print_log, print_except
from datetime import datetime
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

def check_file_size(url):
    try:
        video = pafy.new(url)
        best = video.getbest()
        if best.get_filesize() >= 50000000:
          return (1)
        else:
          return (0)
    except:
        pass

def get_link(url, message, bot, chatid):
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
        return
    except Exception as error:
        print_except(error, chatid, url, bot)

def download(typem, case, chatid, url, message, bot, lurl):
    msg = bot.send_message(chatid, 'Progress: ' + replies.CHK_FILE_SIZE)
    if typem == 'video':
        if check_file_size(url) == 1:
            bot.edit_message_text('Progress: ' + replies.FILE_TOO_BIG, msg.chat.id, msg.message_id)
            time.sleep(0.5)
            bot.edit_message_text('Progress: ' + replies.GET_DWLINK, msg.chat.id, msg.message_id)
            get_link(url, message, bot, chatid)
            time.sleep(0.5)
            bot.edit_message_text('Progress: ' + replies.DONE, msg.chat.id, msg.message_id)
            return
    try:
        now = datetime.now()
        date = now.strftime("%d%m%Y" + "%H%M%S")
        print_log(typem, case, chatid, url, message, bot)
        bot.edit_message_text('Progress: ' + replies.OTW, msg.chat.id, msg.message_id)
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
        bot.edit_message_text('Progress: ' + replies.DOWNLOADING, msg.chat.id, msg.message_id)
        try:
            with ydl:
                ydl.download(lurl)
        except youtube_dl.utils.DownloadError:
            print_log(typem, 'D_ERROR', chatid, url, message, bot)
            return
        filename = getfilename(date, chatid, url, bot)
        file = open(filename, 'rb')
        if typem == 'video':
            bot.edit_message_text('Progress: ' + replies.SND_VIDEO, msg.chat.id, msg.message_id)
            bot.send_video(chatid, file)
        if typem == 'audio':
            bot.edit_message_text('Progress: ' + replies.SND_AUDIO, msg.chat.id, msg.message_id)
            bot.send_audio(chatid, file)
        os.remove(filename)
        bot.edit_message_text('Progress: ' + replies.DONE, msg.chat.id, msg.message_id)
    except:
        try:
            if typem == 'video':
                bot.edit_message_text(replies.FILE_TOO_BIG + '\n' + 'Progress: ' + replies.GET_DWLINK, msg.chat.id, msg.message_id)
                os.remove(filename)
                get_link(url, message, bot, chatid)
                bot.edit_message_text('Progress: ' + replies.DONE, msg.chat.id, msg.message_id)

        except Exception as error:
            if filename:
                os.remove(filename)
            print_except(error, chatid, url, bot)
