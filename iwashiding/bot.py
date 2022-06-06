import os as _os
import re as _re
from dotenv import load_dotenv as _load_dotenv
import discord as _discord
from discord.ext import commands as _commands

COMMAND_PREFIX = ";"
emotes = {"PogChamp": "https://static-cdn.jtvnw.net/emoticons/v2/305954156/static/light/3.0",
          ":)":"https://static-cdn.jtvnw.net/emoticons/v2/1/static/light/1.0",
          ":(":"https://static-cdn.jtvnw.net/emoticons/v2/555555558/static/light/1.0",
          ":O":"https://static-cdn.jtvnw.net/emoticons/v2/555555580/static/light/1.0"}
bot = _commands.Bot(command_prefix=COMMAND_PREFIX)

_load_dotenv()
DISCORD_TOKEN = _os.environ['DISCORD_TOKEN']

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return
    
    if message.content.startswith(COMMAND_PREFIX + 'demo'):
        await demo(await bot.get_context(message))
        return
    if message.content.startswith(COMMAND_PREFIX + 'emote '):
        await emote(await bot.get_context(message), message.content[message.content.index(' ') + 1:])
        return
    
    potential_emotes = _re.findall(r"(:(?:\w|[0-9])+:)", message.content)
    if len(potential_emotes) == 0:
        # no emotes to process
        return
    
    for potential_emote in potential_emotes:
        
        potential_emote = potential_emote[1:-1]
        ctx = await bot.get_context(message)
        
        if potential_emote in emotes:
            await emote(ctx, potential_emote)
            continue
        
        await ctx.send('Emote not found!')

@bot.command()
async def demo(ctx):
    await ctx.send('You should see the PogChamp lizard.')
    await ctx.send(emotes["PogChamp"])

@bot.command()
async def emote(ctx, emote):
    await ctx.send(emotes[emote])

bot.run(DISCORD_TOKEN)