import os as _os
import re as _re
import requests as _requests
from dotenv import load_dotenv as _load_dotenv
from discord.ext import commands as _commands
import discord as _discord

BOT_NAME = "IWasHiding"
SEP = "_"
BOT_DESCRIPTION = "Use popular twitch.tv emotes in discord!"
COMMAND_PREFIX = ";"
emotes = {"PogChamp": "https://static-cdn.jtvnw.net/emoticons/v2/305954156/static/light/1.0",
          ":)":"https://static-cdn.jtvnw.net/emoticons/v2/1/static/light/1.0",
          ":(":"https://static-cdn.jtvnw.net/emoticons/v2/555555558/static/light/1.0",
          ":O":"https://static-cdn.jtvnw.net/emoticons/v2/555555580/static/light/1.0",
          "BibleThump":"https://static-cdn.jtvnw.net/emoticons/v2/86/static/light/1.0",
          ":D":"https://static-cdn.jtvnw.net/emoticons/v2/3/static/light/1.0",
          ":P":"https://static-cdn.jtvnw.net/emoticons/v2/12/static/light/1.0",
          ":|":"https://static-cdn.jtvnw.net/emoticons/v2/555555563/static/light/1.0",
          "<3":"https://static-cdn.jtvnw.net/emoticons/v2/555555584/static/light/1.0"}
TOP_EMOTES_URL = 'https://raw.githubusercontent.com/nouturnsign/iwashiding/master/top_emotes.json'
emotes.update(_requests.get(TOP_EMOTES_URL).json()['emotes'])
bot = _commands.Bot(
    command_prefix=COMMAND_PREFIX, 
    description=BOT_DESCRIPTION,
    help_command=_commands.DefaultHelpCommand(no_category = 'Commands')
)
emoji_cache = {}

_load_dotenv()
DISCORD_TOKEN = _os.environ['DISCORD_TOKEN']

@bot.event
async def on_connect():
    global emoji_cache
    emoji_cache = {emoji.name[len(BOT_NAME + SEP):]: emoji for emoji in bot.emojis if emoji.name.startswith(BOT_NAME)}
    print(BOT_NAME + " connected")
    print("Available emojis:", list(emoji_cache.keys()))

@bot.event
async def on_ready():
    print(BOT_NAME + " ready")

@bot.event
async def on_message(message):
    
    author = message.author
    if not isinstance(author, _discord.member.Member):
        # ignore messages from bots
        return

    if message.content.startswith(COMMAND_PREFIX):
        try:
            await bot.process_commands(message)
        except _commands.errors.CommandNotFound:
            ctx = await bot.get_context(message)
            await ctx.send(f'Command not found. Use {COMMAND_PREFIX}help for help.')
        finally:
            return
    
    await _replace_with_emotes(message)

@bot.command()
async def demo(ctx):
    """Demo of sending emotes."""
    await ctx.send('You should see the PogChamp lizard.')
    await ctx.send(emotes["PogChamp"])

@bot.command()
async def catjam(ctx):
    """Sending catJAM as an embeded gif."""
    await ctx.send(embed = _discord.Embed().set_image(url="https://cdn.betterttv.net/emote/61fe27dd06fd6a9f5be371a2/1x.gif"))    

@bot.command()
async def emote(ctx, emote):
    """Have the bot send the emote as an image/*."""
    
    if emote not in emotes:
        await ctx.send('Emote unavailable.')
        return
        # r = _requests.get(f'https://www.frankerfacez.com/emoticons/?q={emote}&sort=count-desc&days=0')
        # tr = _bs4.BeautifulSoup(r.content, 'html.parser').find('tbody').find('tr')
        # if tr.get_text() == 'No Emotes Found':
        #     await ctx.send('No Emotes Found')
        #     return
        # name = tr.find('td', {'class': 'emote-name'}).a.get_text()
        # src = tr.find('td', {'class': 'emoticon dark'}).img['src']
        # emotes[name] = src
    
        # if emote != name:
        #     await ctx.send(f'{emote} seems to match {name}. Did you mean {name}?') 
        #     return
    
    await ctx.send(emotes[emote])
    
async def _replace_with_emotes(message):

    author = message.author
        
    potential_emotes = _re.findall(r"(:(?:\w|[0-9])+:)", message.content)
    if len(potential_emotes) == 0:
        # no emotes to process
        return

    print('Found emotes:', potential_emotes)
    edited_message = message.content
    ctx = await bot.get_context(message)
    guild = ctx.guild
    
    print('Original message', edited_message)
    for potential_emote in potential_emotes:
        name = potential_emote[1:-1]
        if name not in emoji_cache:
            image_request = _requests.get(emotes[name])
            if image_request.status_code == 200:
                temp_emoji = await guild.create_custom_emoji(name=BOT_NAME + SEP + name, image=image_request.content)
                emoji_cache[name] = temp_emoji
                print('Created emoji:', temp_emoji)
        emoji = emoji_cache[name]
        edited_message = edited_message.replace(potential_emote, str(emoji))
    print('Edited message', edited_message)

    hook = await message.channel.create_webhook(name=BOT_NAME + SEP + "hook")
    print('Created hook:', hook)
    await hook.send(
        edited_message,
        username=author.display_name + " // " + BOT_NAME,
        avatar_url=author.avatar_url
    )
    print('Sent message as hook')
    await message.delete()
    await hook.delete()
    print('Deleted original message and hook')
    
async def _clear_emoji_cache():
    for _, emoji in emoji_cache:
        await emoji.delete()

bot.run(DISCORD_TOKEN)