# Discord Music Bot
Discord bot that allows playing YouTube music in a voice channel. The bot accepts commands to add songs to the playlist, play the next song, pause, resume, stop, and leave the voice channel.

The bot uses the discord.py library to communicate with the Discord API and the yt_dlp library to download and convert the audio of YouTube videos to the MP3 format. Additionally, the code uses regular expressions to extract the YouTube video ID from a search query.

The bot maintains a playlist of songs, which is updated with new song requests from users. When the playlist is not empty, the bot plays the next song on the list in a continuous loop until the playlist is empty or the bot is interrupted.

## Install
#### Dependencies

Install the dependencies
```sh
pip install discord.py yt_dlp
``` 

#### FFMPEG

FFMPEG is crucial to this bot works, so install it before use the bot
If you're using windows, remember to add to Path

Windows:
```sh
https://www.ffmpeg.org/download.html#build-windows
```

MacOS
```sh
brew install ffmpeg
``` 

Linux (Ubuntu)
```sh
sudo apt-get install ffmpeg
``` 
