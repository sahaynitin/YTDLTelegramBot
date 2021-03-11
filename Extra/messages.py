from Extra.classes import bcolors, replies

# url: Content URL [str]
# typem: Type Of Petition [MP3, MP4, ID]
# case: STATUS [OK or TYPE_ERROR]
# chatid: ID of the chat [message.chat.id]
# bot: API Token from Telebot
# message: message handler for reply_to
# progress: Progress of the download
# error_status: Error Status [1: URL_ERROR | 2: SUPP_ERROR]

def print_log_simple(typem, chatid):
	print('\n' + bcolors.WARNING + 'REQUEST FOR ' + typem + ' CREATED\n'
	+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + bcolors.ENDC)

def print_log(typem, case, chatid, url, message, bot):
	if case == 'OK':
		print('\n' + bcolors.WARNING + 'REQUEST FOR ' + typem + ' CREATED\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
		+ bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url + '\n'
		+ bcolors.ENDC)

	if case == 'URL_ERROR':
		print('\n' + bcolors.FAIL + 'REQUEST FOR ' + typem + ' FAILED: No URL\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + bcolors.ENDC)
		reply_error(message, 1, bot)
		return

	if case == 'SUPP_ERROR':
		print('\n' + bcolors.FAIL + 'REQUEST FOR ' + typem + ' FAILED: Invalid URL\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
		+ bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url + bcolors.ENDC)
		reply_error(message, 2, bot)
		return

	if case == 'D_ERROR':
		print('\n' + bcolors.FAIL + 'DOWNLOAD OF ' + typem + ' FAILED: Unsupported URL\n'
		+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
		+ bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url + bcolors.ENDC)
		bot.send_message(chatid, replies.DWN_ERROR)
		return

def print_except(exception, chatid, url, bot):
	print('\n' + bcolors.FAIL + 'Exception ERROR: ' + str(exception) + '\n'
	+ bcolors.OKGREEN + 'Chat ID: '+ bcolors.OKCYAN + str(chatid) + '\n'
	+ bcolors.OKGREEN + 'URL: '+ bcolors.OKCYAN + url + bcolors.ENDC)
	bot.send_message(chatid, replies.EXC_ERROR)
	return

def reply_error(message, error_status, bot):
	if error_status == 1:
		bot.reply_to(message, replies.URL_ERROR)
		return

	if error_status == 2:
		bot.reply_to(message, replies.SUPP_ERROR)
		return
