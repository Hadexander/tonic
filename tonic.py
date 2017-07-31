__author__ = 'Hadexander'
__version__ = '0.0.1'

import discord
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
        await ctx.bot.send_message(ctx.message.channel, 'You do not have sufficient access to use this command.')
    else:
        print('Unhandled exception: %s' %(type(error)))

@command(pass_context=True)
async def info(ctx):
    """Shows general information about me."""
    msg = """```Hello, I am Tonic v%s - your diligent bartender.\n
I am using discord.py v%s.\n
I am currently servicing %s servers.\n
Please report any issues to my author: %s\n
Use %shelp to get a list of commands.```"""\
    %(__version__, discord.__version__, len(ctx.bot.servers), __author__, await serverwide_prefix(ctx.message.server))
    await ctx.bot.send_message(ctx.message.channel, msg)

bot.add_command(inspire)
bot.add_command(access)
bot.add_command(avatar)
bot.add_command(info)
bot.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')
