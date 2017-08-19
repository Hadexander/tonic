import discord
from discord.ext import commands
import sys

@commands.command(pass_context=True)
async def upgrade(ctx):
    """Exits Tonic in order for Gin to git pull and relaunch"""
    await sys.exit(1)