import asyncio
import aiohttp
import discord
from discord.ext import commands

@commands.command(pass_context=True)
async def inspire(ctx):
    """Get a random inspirational image, courtsey of inspirobot.me"""
    async with aiohttp.ClientSession() as session:
        async with session.get('http://inspirobot.me/api?generate=true') as response:
            if(response.status == 200):
                imgurl = await response.text()
                embed = discord.Embed(colour=discord.Colour.dark_blue())
                embed.set_image(url=imgurl)
                embed.set_footer(text='http://inspirobot.me/')
                await ctx.bot.send_message(ctx.message.channel, embed=embed)
