import random
import asyncio
import aiohttp
import discord
import re
from discord.ext import commands
from discord.ext.commands import BadArgument
from lxml import html
import requests

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

    _dice = re.compile(r'^(\d+)?d(\d+)([+-]\d+)?')
    _dicelimit = 100
    _displaylimit = 20
    @commands.command(pass_context=True)
    async def roll(self, ctx, NdM):
        """Roll N dice with M sides each. Supports dice notation NdM[+-X]"""
        response = "Rolled {}: **{}**"
        match = self._dice.match(NdM)
        if not match:
            raise BadArgument()
        args = match.groups()
        n = args[0]
        m = args[1]
        x = args[2]
        if n:
            n = int(n)
            if n <= 0 or n > self._dicelimit:
                raise BadArgument()
        else:
            n = 1
        m = int(m)
        if m <= 0:
            raise BadArgument()
        rolls = [random.randint(1, m) for i in range(n)]
        result = sum(rolls)
        if x:
            x = int(x)
            result += x
        response = response.format(NdM, result)
        if n <= self._displaylimit:
            response += "\n{}".format(str(rolls))
        await ctx.bot.send_message(ctx.message.channel, response.format(NdM, result))

    @commands.command(pass_context=True)
    async def watdo(self, ctx, *args):
        """Ask Tonic to randomly pick from a specified list of options."""
        choicelist = []
        for choice in args:
            choicelist.append(choice)
        result = random.choice(choicelist)
        await ctx.bot.send_message(ctx.message.channel, "I pick {}!".format(result))

    @commands.command(pass_context=True)
    async def deal(self, ctx):
        """A dank meme."""
        frames = ['( •_•)', '( •_•)>⌐■-■', '(⌐■_■)', '(⌐■_■) Deal', '(⌐■_■) Deal with', '(⌐■_■) Deal with it.']
        msg = await ctx.bot.send_message(ctx.message.channel, frames[0])
        for frame in frames[1:]:
            await asyncio.sleep(1)
            await ctx.bot.edit_message(msg, frame)

    @commands.command(pass_context=True)
    async def bother(self, ctx, user: discord.Member):
        """A very mean thing to do."""
        for i in range(5):
            msg =  await ctx.bot.send_message(ctx.message.channel, user.mention)
            await ctx.bot.delete_message(msg)

    @commands.command(pass_context=True)
    async def drinkify(self,ctx):
        """Ask Tonic for a drink inspired by your favorite artists!"""
        artist = ctx.message.content[9:]
        drink = ""
        response = requests.get('http://drinkify.org/{}'.format(artist))
        if response.status_code == 200:
            root = html.fromstring(response.content)
            recipe = root.xpath('//ul[@class="recipe"]/li/text()')
            for alc in recipe:
                drink +="{}\n".format(alc)
            instructions = root.xpath('normalize-space(//p[@class="instructions"]/text())')
            drink += "\nInstructions:\n{}".format(instructions)
        else:
            return
        await ctx.bot.send_message(ctx.message.channel, drink)
