import discord
from discord.ext import commands
import sys

@commands.command(pass_context=True)
async def upgrade(ctx):
    """Exits Tonic in order for Gin to git pull and relaunch"""
    msg = 'Okay! I\'ll check for an upgrade now!' 
    await ctx.bot.send_message(ctx.message.channel, msg)
    await sys.exit(1)
