class bcolors: #COLORS CLASS FOR COLOR CODING PRINT LOGS
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class replyes:
    HELP = ('/start: Display a welcome message and credits\n'+
	       '/help: Display all commands available with descriptions\n' +
	       '/dl: Download a video [/dl URL]\n' +
           '/dlmp3: Download a video on mp3 [/dlmp3 URL]\n' +
           '/id: Get the video ID [/id URL]')
    WELCOME = 'Hi!! 👋\n' + 'Welcome to the YTDL Bot made by @galisteo02!!'
    DISCLAIMER = '⚠️ DISCLAIMER ⚠️\n'+ '\n' + '🆔 not always corresponds to the real one!!'
    ID = '🆔 ==> '
    URL_ERROR = 'No URL given ❌'
    SUPP_ERROR = 'Invalid URL given ❌'
    OTW = 'On the way! 👌'
    DOWNLOADING = 'Downloading... ⬇️'
    SND_AUDIO = 'Sending audio... ⬆️'
    SND_VIDEO = 'Sending video... ⬆️'
    DONE = 'Done! ✅'
    DWN_ERROR = 'Download ERROR! Unsupported URL ❌'
