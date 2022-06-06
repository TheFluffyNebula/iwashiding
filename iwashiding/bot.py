import os as _os
from dotenv import load_dotenv as _load_dotenv
import discord as _discord
from discord.ext import commands as _commands
import json as _json

with open("emotes.json") as f:
   emotes = _json.load(f)["emotes"]
bot = _commands.Bot(command_prefix=";")
_load_dotenv()
DISCORD_TOKEN = _os.environ['DISCORD_TOKEN']

@bot.command()
async def demo(ctx):
    await ctx.send('Looks like things are working?')

@bot.command()
async def emote(ctx, emote):
    await ctx.send(emotes[emote])

bot.run(DISCORD_TOKEN)