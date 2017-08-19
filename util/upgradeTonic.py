import discord
from discord.ext import commands
import sys

@commands.command(pass_context=True)
async def blaze_it(ctx):
    """Exits Tonic in order for Gin to git pull and relaunch"""
    msg = 'Gotchu fam! Shit\'s lit, let me hit this blunt, be right back!'
    await ctx.bot.send_message(ctx.message.channel, msg)
    await discord.Client().close()
    sys.exit(420)