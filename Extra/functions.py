import youtube_dl

def is_supported(url): #CHECK IS URL IS SUPPORTED
    if 'vm.tiktok.com' in url:
        return True
    else:
        ies = youtube_dl.extractor.gen_extractors()
        for ie in ies:
            if ie.suitable(url) and ie.IE_NAME != 'generic':
                return True
        return False
