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

class replies: #TEXT FOR REPLIES
    HELP = ('/start: Display welcome message!\n'+
	       '/help: Display all commands available with descriptions\n' +
           '/errors: Display info about the errors that can happen\n')
    HOW_TO = ('Just send a URL to the bot and select a download option, no commands, just a message 😎\n' +
              'The bot will take care of the rest 👨🏻‍🔧')
    NEW_WAY = 'There is a new way to download!! Check it out ⬇️'
    WELCOME = ('Hi!! 👋🏻\n' +
               'Welcome to THE DOWNLOADER 👨🏻‍🔧⬇️ made by @galisteo02 ✌️🏻')
    ERRORS = ('🚨 No URL given 🚨: You haven\'t given a URL\n'+
	       '🚨 Invalid URL given 🚨: You have given an invalid URL\n' +
	       '🚨 DOWNLOAD ERROR! 🚨: Video couldn\'t be downloaded due to an unexpected YTDL error, try again later. '
           'Remember it´s not possible to download Instagram videos\n' +
           '🚨 EXCEPTION ERROR 🚨: Exception raised in code (contact @galisteo02 so it can get fixed)')
    URL_ERROR = '🚨 No URL given 🚨'
    SUPP_ERROR = '🚨 Invalid URL given 🚨'
    OTW = 'On the way! 👌🏻'
    DOWNLOADING = '⬇️ Downloading ⬇️'
    SND_AUDIO = '⬆️ Sending audio ⬆️'
    SND_VIDEO = '⬆️ Sending video ⬆️'
    CHK_FILE_SIZE = 'Checking File Size 🧐'
    FILE_TOO_BIG = 'File too big! 😞'
    GET_DWLINK = 'Getting Download Link...🔗'
    DONE = '✅ Done ✅'
    DWN_ERROR = '🚨 DOWNLOAD ERROR! 🚨'
    EXC_ERROR = '🚨 EXCEPTION ERROR! 🚨'
