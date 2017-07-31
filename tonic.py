__author__ = 'Hadexander'
__version__ = '0.0.1'

import discord
import random
from discord.ext.commands import *
from extras import *
from util import *

bot = Bot(command_prefix)

@bot.event
async def on_ready():
    print('Ready (%s:%s)' % (bot.user.name, bot.user.id))

@bot.event
async def on_command_error(error, ctx):
    if(isinstance(error, VerificationError)):
        nope = ['No.', 'Nope.', 'Nah.', 'Nu.', 'Your access level isn\'t high enough.']
        await ctx.bot.send_message(ctx.message.channel, random.choice(nope))
    elif(isinstance(error, (MissingRequiredArgument, BadArgument))):
        help = bot.commands.get('help')
        await help.callback(ctx, ctx.command.name)
    else:
        print('Unhandled exception: %s' %(type(error)))

@command(pass_context=True)
async def info(ctx):
    """Shows general information about me."""
    msg = """```Hello, I am Tonic v%s - your diligent bartender.
I am using discord.py v%s.
I am currently servicing %s servers.
Please report any issues to my author: %s
Use %shelp to get a list of commands.```"""\
    %(__version__, discord.__version__, len(ctx.bot.servers), __author__, ctx.prefix)
    await ctx.bot.send_message(ctx.message.channel, msg)

bot.add_command(inspire)
bot.add_command(access)
bot.add_command(avatar)
bot.add_command(info)
bot.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')
