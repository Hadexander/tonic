import asyncio
import aiohttp
from discord.ext import commands

@commands.command(pass_context=True)
async def inspire(ctx):
    """Get a random inspirational image, courtsey of inspirobot.me"""
    async with aiohttp.ClientSession() as session:
        async with session.get('http://inspirobot.me/api?generate=true') as response:
            if(response.status == 200):
                imgurl = await response.text()
                await ctx.bot.send_message(ctx.message.channel, imgurl)