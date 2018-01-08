#! /usr/bin/python3
import random
import traceback
from discord.ext.commands import Bot, MissingRequiredArgument, BadArgument, NoPrivateMessage
import core
from util.prefix import command_prefix
from util.checks import VerificationError
from storage.lookups import get_setting

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

core.setup(bot)
apikey = get_setting('discord_api_key')
bot.run(apikey.value)
