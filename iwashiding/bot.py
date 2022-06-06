import os as _os
from dotenv import load_dotenv as _load_dotenv
import discord as _discord
from discord.ext import commands as _commands

bot = _commands.Bot(command_prefix=">")
_load_dotenv()
DISCORD_TOKEN = _os.environ['DISCORD_TOKEN']
bot.run(DISCORD_TOKEN)