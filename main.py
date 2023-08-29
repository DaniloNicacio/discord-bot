import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import os
import asyncio
import urllib.request
import re


intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Connected as {bot.user.name}')

@bot.slash_command()
async def hello(ctx):
    await ctx.send('Olá, mundo!')

bot.run('')
