from Extra.classes import bcolors
from Extra.checks import is_supported
import telebot
bot = telebot.TeleBot("***REMOVED***") #OG BOT
#bot = telebot.TeleBot("***REMOVED***") #TEST BOT

# typep: Type Of Petition [MP3, MP4, ID]
# case: ERROR or OK
# chat_id: ID of the chat [message.chat.id]
# cid: Content ID
# url: URL from the request
# message: message

def print_log_simple(typep, chat_id):
	print(bcolors.WARNING + 'REQUEST FOR ' + typep + ' CREATED\n' +
	bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chat_id) + '\n'
	+ bcolors.ENDC)

def print_log(typep, case, chat_id, cid, url, message):
	if case == 'OK':
		print(bcolors.WARNING + 'REQUEST FOR ' + typep + ' CREATED\n' +
		bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chat_id) + '\n' +
		bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url[-1] + '\n' +
		bcolors.OKGREEN + 'ID: ' + bcolors.OKCYAN + cid[-1] + '\n' 
		+ bcolors.ENDC)

	if case == 'ERROR':
		if not url:
			print(bcolors.FAIL + 'REQUEST FOR ' + typep + ' FAILED: NO URL GIVEN\n' +
			bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chat_id) + '\n'
			+ bcolors.ENDC)
		
			reply_error(message, 1)
			return

		if not is_supported(url[-1]):
			print(bcolors.FAIL + 'REQUEST FOR ' + typep + ' FAILED: INVALID URL GIVEN\n' +
			bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chat_id) + '\n'
			+ bcolors.ENDC)

			reply_error(message, 2)
			return

def reply_error(message, error_status):
	if error_status == 1:
		bot.reply_to(message, 'No URL given :(')
		return

	if error_status == 2:
		bot.reply_to(message, 'Invalid URL given :(')
		return