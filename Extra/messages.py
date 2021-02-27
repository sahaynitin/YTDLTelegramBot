from Extra.classes import bcolors, replies
import telebot
bot = telebot.TeleBot("***REMOVED***") #OG BOT
#bot = telebot.TeleBot("***REMOVED***") #TEST BOT

# typem: Type Of Petition [MP3, MP4, ID]
# case: ERROR or OK
# chatid: ID of the chat [message.chat.id]
# cid: Content ID
# url: URL from the request
# message: message

def print_log_simple(typem, chatid):
	print(bcolors.WARNING + 'REQUEST FOR ' + typem + ' CREATED\n'
	+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
	+ bcolors.ENDC)

def print_log(typem, case, chatid, cid, url, message):
	if case == 'OK':
		print(bcolors.WARNING + 'REQUEST FOR ' + typem + ' CREATED\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
		+ bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url[-1] + '\n'
		+ bcolors.OKGREEN + 'ID: ' + bcolors.OKCYAN + cid[-1] + '\n'
		+ bcolors.ENDC)

	if case == 'URL_ERROR':
		print(bcolors.FAIL + 'REQUEST FOR ' + typem + ' FAILED: No URL\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
		+ bcolors.ENDC)
		reply_error(message, 1)
		return

	if case == 'SUPP_ERROR':
		print(bcolors.FAIL + 'REQUEST FOR ' + typem + ' FAILED: Invalid URL\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
		+ bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url[-1] + '\n'
		+ bcolors.ENDC)
		reply_error(message, 2)
		return

	if case == 'D_ERROR':
		print(bcolors.FAIL + 'DOWNLOAD OF ' + typem + ' FAILED: Unsupported URL\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
		+ bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url[-1] + '\n'
		+ bcolors.ENDC)
		progress_msg(chatid, 5, typem)
		return

def reply_error(message, error_status):
	if error_status == 1:
		bot.reply_to(message, replies.URL_ERROR)
		return

	if error_status == 2:
		bot.reply_to(message, replies.SUPP_ERROR)
		return

def progress_msg(chatid, progress, typem):
	if progress == 1:
		bot.send_message(chatid, replies.OTW)
		return
	if progress == 2:
		bot.send_message(chatid, replies.DOWNLOADING)
		return
	if progress == 3:
		if typem == 'dl':
			bot.send_message(chatid, replies.SND_VIDEO)
			return
		if typem == 'dlmp3':
			bot.send_message(chatid, replies.SND_AUDIO)
			return
	if progress == 4:
		bot.send_message(chatid, replies.DONE)
		return
	if progress	== 5:
		bot.send_message(chatid, replies.DWN_ERROR)
