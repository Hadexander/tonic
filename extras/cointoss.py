import discord
from discord.ext import commands
import random

@commands.command(pass_context=True)
async def flipcoin(ctx):
    """Flip a coin."""
    flip = random.choice([True, False])
    if flip == True:
        msg = 'It\'s heads!'
        await ctx.bot.send_message(ctx.message.channel, msg)
    elif flip == False:
        msg = 'It\'s tails!'
        await ctx.bot.send_message(ctx.message.channel, msg)