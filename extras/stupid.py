import asyncio
from discord.ext import commands

@commands.command(pass_context=True)
async def deal(ctx):
    """A dank meme."""
    frames = ['( •_•)', '( •_•)>⌐■-■', '(⌐■_■)', '(⌐■_■) Deal', '(⌐■_■) Deal with', '(⌐■_■) Deal with it.']
    msg = await ctx.bot.send_message(ctx.message.channel, frames[0])
    for frame in frames[1:]:
        await asyncio.sleep(1)
        await ctx.bot.edit_message(msg, frame)
