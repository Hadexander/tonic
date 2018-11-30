#!/usr/bin/env python3
import random
import traceback
import pkgutil
import importlib
from discord.ext.commands import Bot, MissingRequiredArgument, BadArgument, NoPrivateMessage, CommandNotFound
from util.prefix import command_prefix
from util.checks import VerificationError
from storage import settings
from storage.db import DatabaseInterface

bot = Bot(command_prefix)

dburl = settings.load('Database').get('url')
bot.database = DatabaseInterface(dburl)
steamurl = settings.load('Database').get('url')
bot.steamdb = DatabaseInterface(steamurl)
# event code remains here for now
sass = ["I don't {} your {}.", "I can't {} a {}, you donut.",
        "No, you {} your {}.", "You should know that I can't {} a {} just like that..."]
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
        traceback.print_exception(type(error), error, error.__traceback__)

# load submodules
startup_modules = []

print("Loading submodules...")
for finder, name, ispkg in pkgutil.iter_modules('.'):
    if ispkg:
        try:
            module = importlib.import_module(name)
            if hasattr(module, 'setup'):
                startup_modules.append(name)
        except Exception as ex:
            print("[{}] could not be imported. Reason:\n{} {}".format(name, type(ex), str(ex)))

print("Installing cogs...")
for name in startup_modules:
    bot.load_extension(name)

token = settings.load('Discord').get('token')
bot.run(token)
