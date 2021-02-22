import youtube_dl
import os

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
