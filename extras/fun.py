import random
import asyncio
import aiohttp
import discord
from discord.ext import commands

class Fun:
    @commands.command(pass_context=True)
    async def inspire(self, ctx):
        """Get a random inspirational image, courtsey of inspirobot.me"""
        async with aiohttp.ClientSession() as session:
            async with session.get('http://inspirobot.me/api?generate=true') as response:
                if(response.status == 200):
                    imgurl = await response.text()
                    embed = discord.Embed(colour=discord.Colour.dark_blue())
                    embed.set_image(url=imgurl)
                    embed.set_footer(text='http://inspirobot.me/')
                    await ctx.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def flipcoin(self, ctx):
        """Flip a coin."""
        flip = random.choice([True, False])
        if flip == True:
            msg = 'It\'s heads!'
            await ctx.bot.send_message(ctx.message.channel, msg)
        elif flip == False:
            msg = 'It\'s tails!'
            await ctx.bot.send_message(ctx.message.channel, msg)

    @commands.command(pass_context=True)
    async def rolldie(self, ctx, call):
        """Roll a die with a specified number of faces."""
        erresponses = ["I don't roll your {}.", "I don't have any {} die.", "I can't roll a {}, you donut."]
        response = "Rolling d{} ... \n {}"
        if call.isdigit() and call!=0:
            result = random.randrange(1,int(call))
            await ctx.bot.send_message(ctx.message.channel, response.format(call, result))
        elif call[:1] == 'd' and call[1:].isdigit():
            result = random.randrange(1,int(call[1:]))
            await ctx.bot.send_message(ctx.message.channel, response.format(call[1:], result))
        else:
            await ctx.bot.send_message(ctx.message.channel, random.choice(erresponses).format(call))

    @commands.command(pass_context=True)
    async def deal(self, ctx):
        """A dank meme."""
        frames = ['( •_•)', '( •_•)>⌐■-■', '(⌐■_■)', '(⌐■_■) Deal', '(⌐■_■) Deal with', '(⌐■_■) Deal with it.']
        msg = await ctx.bot.send_message(ctx.message.channel, frames[0])
        for frame in frames[1:]:
            await asyncio.sleep(1)
            await ctx.bot.edit_message(msg, frame)
