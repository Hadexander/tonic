import discord
from discord.ext import commands
import sys

@commands.command(pass_context=True)
async def evolve(ctx):
    """Exits Tonic in order for Gin to git pull and relaunch"""
    msg = 'Getting some improvements! I\'ll be back in a sec!'
    await ctx.bot.send_message(ctx.message.channel, msg)
    await discord.Client().close()
    sys.exit(420)