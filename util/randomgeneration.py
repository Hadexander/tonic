import secrets
import discord
from discord.ext import commands

@commands.command(pass_context=True)
async def tonictoken(ctx):
    """Generate random Tonic Token"""
     generatedToken = secrets.token_urlsafe(32)
     await ctx.bot.send_message(ctx.message.channel, generatedToken)