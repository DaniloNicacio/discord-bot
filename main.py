import discord
from discord.ext import commands
import yt_dlp
import os
import asyncio
import urllib.request
import re

# Options for youtube-dlp to download the best audio quality as an MP3 file
ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

# Create a Discord client with the command prefix "&" and enable all intents, you can change the prefix here
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "&",intents=intents)

# List to store the URLs of songs in the playlist
playlist = []

# Helper function to get the YouTube video URL from a search query
def get_video_url(query):
    if "youtube.com" in query:
        url = query
    else:
        search_keyword = query.replace(" ","+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]    
    return url
        
# Command to add a song to the playlist and play it if it's the first song in the list
@client.command()
async def play(ctx, query: str):
    url = get_video_url(query)
    playlist.append(url)
    if len(playlist) == 1:
        
        # If the bot is already connected to a voice channel, move to the author's voice channel. Otherwise, connect to the author's voice channel.
        if ctx.voice_client is not None and ctx.voice_client.is_connected():
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            voice = ctx.voice_client
        else:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
            voice = await voiceChannel.connect()

        # Get the voice client and download the song from the YouTube video URL
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

        # Play the song and start playing the next song in the playlist on a separate thread
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        asyncio.create_task(play_next(ctx))
        
# Function to play the next song in the playlist
async def play_next(ctx):
    while True:
        if len(playlist) > 0:
            # Wait until the current song has finished playing before playing the next song
            if ctx.voice_client is not None and ctx.voice_client.is_playing():
                await asyncio.sleep(5)
                continue
            
            # Remove the current song from the playlist and download the next song from its URL
            if os.path.exists("song.mp3"):
                os.remove("song.mp3")
                playlist.pop(0)
            if len(playlist) > 0:
                url = playlist[0]
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                        
                # Play the next song in the playlist
                ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
        else:
            await asyncio.sleep(5)
           
# Function to leave the voice channel            
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I'm not in any voice channel")

# Function to pause the song
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("We don't have any music playing at the moment")
        
# Function to resume the song
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The music was not paused")

# Function to stop the song and clear the playlist
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()

client.run('Your token goes here')