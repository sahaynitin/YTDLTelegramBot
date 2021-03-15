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

def check_file_size(url, typem):
    try:
        if typem == 'video':
            video = pafy.new(url)
            best = video.getbest()
            if best.get_filesize() >= 50000000:
                return (1)
        if typem == 'audio':
            video = pafy.new(url)
            best = video.getbestaudio()
            if best.get_filesize() >= 50000000:
                return (1)
    except:
        pass

def get_link(url, typem):
    try:
        if typem == 'audio':
            video = pafy.new(url)
            best = video.audiostreams[-1]
            quality = best.quality
            durl = best.url_https
            return quality, durl
        if typem == 'video':
            video = pafy.new(url)
            best = video.streams[-1]
            quality = best.quality
            durl = best.url_https
            return quality, durl
    except:
        pass

def download(typem, case, chatid, url, message, bot, lurl):
    msg = bot.send_message(chatid, '<b>Progress: </b>' + replies.CHK_FILE_SIZE, parse_mode='HTML')
    if check_file_size(url, typem) == 1:
        bot.edit_message_text('<b>Progress: </b>' + replies.FILE_TOO_BIG, msg.chat.id, msg.message_id, parse_mode='HTML')
        bot.edit_message_text('<b>Progress: </b>' + replies.GET_DWLINK, msg.chat.id, msg.message_id, parse_mode='HTML')
        quality, durl = get_link(url, typem)
        link = '<a href=\"' + durl + '\">' + quality + '</a>'
        bot.reply_to(message, 'Quality ' + link, parse_mode='HTML')
        bot.edit_message_text('<b>Progress: </b>' + replies.DONE, msg.chat.id, msg.message_id, parse_mode='HTML') 
        return
    try:
        now = datetime.now()
        date = now.strftime("%d%m%Y" + "%H%M%S")
        print_log(typem, case, chatid, url, message, bot)
        bot.edit_message_text('<b>Progress: </b>' + replies.OTW, msg.chat.id, msg.message_id, parse_mode='HTML')
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
        bot.edit_message_text('<b>Progress: </b>' + replies.DOWNLOADING, msg.chat.id, msg.message_id, parse_mode='HTML')
        try:
            with ydl:
                ydl.download(lurl)
        except youtube_dl.utils.DownloadError:
            print_log(typem, 'D_ERROR', chatid, url, message, bot)
            return
        filename = getfilename(date, chatid, url, bot)
        file = open(filename, 'rb')
        if typem == 'video':
            bot.edit_message_text('<b>Progress: </b>' + replies.SND_VIDEO, msg.chat.id, msg.message_id, parse_mode='HTML')
            bot.send_video(chatid, file)
        if typem == 'audio':
            bot.edit_message_text('<b>Progress: </b>' + replies.SND_AUDIO, msg.chat.id, msg.message_id, parse_mode='HTML')
            bot.send_audio(chatid, file)
        os.remove(filename)
        bot.edit_message_text('<b>Progress: </b>' + replies.DONE, msg.chat.id, msg.message_id, parse_mode='HTML')
    except:
        try:
            bot.edit_message_text(replies.FILE_TOO_BIG + '\n' + '<b>Progress: </b>' + replies.GET_DWLINK, msg.chat.id, msg.message_id, parse_mode='HTML')
            os.remove(filename)
            quality, durl = get_link(url, typem)
            link = '<a href=\"' + durl + '\">' + quality + '</a>'
            bot.reply_to(message, 'Quality ' + link, parse_mode='HTML')
            bot.edit_message_text('<b>Progress: </b>' + replies.DONE, msg.chat.id, msg.message_id, parse_mode='HTML')

        except Exception as error:
            if filename:
                os.remove(filename)
            print_except(error, chatid, url, bot)
