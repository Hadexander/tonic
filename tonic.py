#! /usr/bin/python3
import random
import traceback
from discord.ext.commands import Bot, MissingRequiredArgument, BadArgument, NoPrivateMessage, CommandNotFound
import core
from util.prefix import command_prefix
from util.checks import VerificationError
from storage.lookups import global_settings

bot = Bot(command_prefix)
sass = ["I don't {} your {}.", "I can't {} a {}, you donut.", "No, you {} your {}.", "You should know that I can't {} a {} just like that..."]
nope = ['No.', 'Nope.', 'Nah.', 'Your access level isn\'t high enough.']

@bot.event
async def on_ready():
    print('Ready (%s:%s)' % (bot.user.name, bot.user.id))

@bot.event
async def on_command_error(error, ctx):
    error = getattr(error, 'original', error)

    if(isinstance(error, VerificationError)):
        await ctx.bot.send_message(ctx.message.channel, random.choice(nope))
    elif(isinstance(error, MissingRequiredArgument)):
        help = bot.commands.get('help')
        await help.callback(ctx, ctx.command.name)
    elif(isinstance(error, (CommandNotFound, BadArgument))):
        if len(ctx.args) > 2:
            errmsg = random.choice(sass)
            errmsg = errmsg.format(ctx.command.name, ctx.args[2])
            await ctx.bot.send_message(ctx.message.channel, errmsg)
    elif(isinstance(error, NoPrivateMessage)):
        await ctx.bot.send_message(ctx.message.channel, 'This command must be used in a channel.')
    else:
        traceback.print_exception(type(error), error, None)

core.setup(bot)
bot.run(global_settings().discord_key)
