import discord
from discord.ext.commands import *
from util.prefix import command_prefix

@command(pass_context=True)
async def info(ctx):
    """Shows general information about me."""
    prefixes = command_prefix(ctx.bot, ctx.message)
    msg = """```Hello, I am Tonic - your diligent bartender.
                I am using discord.py v{}.
                I am currently servicing {} servers.
                I respond to messages prefixed with: {}
                Use {}help to get a list of commands.```"""\
    .format(discord.__version__, len(ctx.bot.servers), ' '.join(prefixes), ctx.prefix)\
    .replace(ctx.bot.user.mention, '@'+ctx.bot.user.name)
    await ctx.bot.send_message(ctx.message.channel, msg)