# YTDLTelegramBot
This is a Telegram Bot that implements [youtube-dl](http://ytdl-org.github.io/youtube-dl/) in Telegram. <br/>
With this bot you can download videos from any social network directly through a Telegram chat.

## How can I use it?
To start using it you need to talk to the bot [@YTDL_Tele_Bot](https://t.me/YTDL_Tele_Bot) in Telegram. <br/>
The bot accepts 4 slash commands:
- **/start** --> Sends a welcome message and gives you 3 inline buttons (How to download, Help and Erros Info)
- **/help** --> Sends a message with all commands available with an explanation of each oneof them
- **/howto** --> Sends a message with instructions on how to download a video
- **/errors** --> Sends a message with all the possible erros and a description of them

To download a video just send the video URL and select one of the options given by the bot:
- **MP4** --> Sends you the video in the highest quality possible, in case the video is too big for Telegram it will send you a download URL
- **MP3** --> Sends you the audio of the video in the best quality possible
- **Cancel Download** --> It cancels the download

## Requirements to host your own bot
You will need Python installed, the current required version can be found in [runtime.txt](https://github.com/somedevv/YTDLTelegramBot/blob/master/runtime.txt), 
also all the Python packages needed are in [requiremets.txt](https://github.com/somedevv/YTDLTelegramBot/blob/master/requirements.txt). Also you will need a 
**Telegram Bot Token**, which you can get using the [Bot Father](https://t.me/botfather) in Telegram.
