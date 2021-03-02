import youtube_dl
import os
import telebot
from Extra.messages import print_log, print_log_simple, progress_msg

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

def download(typem, sts, chatid, cid, url, message, bot):
    print_log(typem, sts, chatid, cid, url, message, bot)
    progress_msg(chatid, 1, typem, bot)
    if 'instagram.com' in url[-1]:
        instadl(typem, chatid, cid, url, message, bot)
        return
    if typem == 'video':
        ydl_opts = {
        'outtmpl': cid[-1] + '.%(ext)s',
        }
    if typem == 'audio':
        ydl_opts = {
        'outtmpl': cid[-1] + '.%(ext)s',
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
        print_log(typem, 'D_ERROR', chatid, cid, url, message)
        return
    progress_msg(chatid, 3, typem, bot)
    filename = getfilename(cid[-1])
    file = open(filename, 'rb')
    if typem == 'video':
        bot.send_video(chatid, file)
    if typem == 'audio':
        bot.send_audio(chatid, file)
    os.remove(filename)
    progress_msg(chatid, 4, typem, bot)

def instadl(typem, chatid, cid, url, message, bot):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    try:
        with ydl:
            result = ydl.extract_info(
                url[-1],
                download=False  # We just want to extract the info
            )
        progress_msg(chatid, 6, typem, bot)
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        for i in video['formats']:
            link = '<a href=\"' + i['url'] + '\">' + 'link' + '</a>'

            bot.send_message(chatid, link, parse_mode='HTML', disable_notification=True)
        progress_msg(chatid, 4, typem, bot)
    except Exception as e:
        print_log(typem, 'URL_ERROR', chatid, cid, url, message, bot)
