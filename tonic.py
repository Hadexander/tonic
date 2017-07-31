import discord
from discord.ext.commands import *
from extras import *
from util import *

async def command_prefix(bot, message):
    return [bot.user.mention+' ', '!']

bot = Bot(command_prefix)

@bot.event
async def on_ready():
    print('Logged in (%s:%s)' % (bot.user.name, bot.user.id))

@bot.event
async def on_command_error(error, ctx):
    if(isinstance(error, VerificationError)):
        await ctx.bot.send_message(ctx.message.channel, 'You do not have sufficient access to use this command.')
    else:
        print('Unhandled exception: %s' %(type(error)))

bot.add_command(inspire)
bot.add_command(access)
bot.add_command(avatar)
bot.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')
