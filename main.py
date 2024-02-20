import os
import discord
from discord.ext import commands
import yt_dlp
import urllib.request
import re

ffmpeg_options = {'options': '-vn'}
# Options for youtube-dlp to download the best audio quality as an MP3 file
ydl_opts = {'format': 'bestaudio'}

# Create a Discord client with the command prefix "&" and enable all intents, you can change the prefix here
intents = discord.Intents.all()
client = commands.Bot(command_prefix="&", intents=intents)

def get_audio(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# Helper function to get the YouTube video URL from a search query
def get_video_url(query):
    if "youtube.com" in query:
        url = query
    else:
        search_keyword = query.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
    return url

# Command to add a song to the playlist and play it if it's the first song in the list
@client.command()
async def play(ctx, query: str):
    try:
        if ctx.voice_client and ctx.voice_client.is_connected():
            # If the bot is already connected to a voice channel, simply add the music to the playlist
            url = get_video_url(query)
            song = get_audio(url)
            ctx.voice_client.play(discord.FFmpegPCMAudio(song["url"], **ffmpeg_options))
        else:
            # If the bot is not connected to a voice channel, connect to the author's voice channel and play the music
            if ctx.author.voice:
                voiceChannel = ctx.author.voice.channel
                await voiceChannel.connect()
                url = get_video_url(query)
                song = get_audio(url)
                ctx.voice_client.play(discord.FFmpegPCMAudio(song["url"], **ffmpeg_options))
            else:
                await ctx.send("You need to be in a voice channel to use this command.")
    except AttributeError:
        await ctx.send("Couldn't play the music.")

# Function to leave the voice channel
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect(force=True)
    else:
        await ctx.send("I'm not in any voice channel")


# Function to pause the song
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("We don't have any music playing at the moment")


# Function to resume the song
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The music was not paused")


# Function to stop the song and clear the playlist
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

DISCORD_TOKEN = os.getenv("DISCORD_API")
client.run(DISCORD_TOKEN)