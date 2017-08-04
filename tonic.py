__author__ = 'Hadexander'
__version__ = '0.0.1'

import discord
import random
import traceback
from discord.ext.commands import *
from extras import *
from util import *
from github import *
from poe import *

bot = Bot(command_prefix)

@bot.event
async def on_ready():
    print('Ready (%s:%s)' % (bot.user.name, bot.user.id))

@bot.event
async def on_command_error(error, ctx):
    if(isinstance(error, VerificationError)):
        nope = ['No.', 'Nope.', 'Nah.', 'Your access level isn\'t high enough.']
        await ctx.bot.send_message(ctx.message.channel, random.choice(nope))
    elif(isinstance(error, (MissingRequiredArgument, BadArgument))):
        help = bot.commands.get('help')
        await help.callback(ctx, ctx.command.name)
    elif(isinstance(error, NoPrivateMessage)):
        await ctx.bot.send_message(ctx.message.channel, 'This command must be used in a channel.')
    else:
        traceback.print_exception(type(error), error, None)

@command(pass_context=True)
async def info(ctx):
    """Shows general information about me."""
    prefixes = await command_prefix(ctx.bot, ctx.message)
    msg = """```Hello, I am Tonic v{} - your diligent bartender.
I am using discord.py v{}.
I am currently servicing {} servers.
Please report any issues to my author: {}
I respond to messages prefixed with: {}
Use {}help to get a list of commands.```"""\
    .format(__version__, discord.__version__, len(ctx.bot.servers), __author__, ' '.join(prefixes), ctx.prefix)\
    .replace(ctx.bot.user.mention, '@'+ctx.bot.user.name)
    await ctx.bot.send_message(ctx.message.channel, msg)

bot.add_command(inspire)
bot.add_command(access)
bot.add_command(avatar)
bot.add_command(info)
bot.add_command(prefix)
bot.add_command(gitprofile)
bot.add_command(mygit)
bot.add_command(tonictoken)
bot.add_command(poewiki)
bot.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')
