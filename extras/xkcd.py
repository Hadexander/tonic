import asyncio
import aiohttp
import xkcd
import discord
from discord.ext import commands

class Xkcd:
    @commands.command(name='xkcd', pass_context=True)
    async def getxkcd(self, ctx, call='random'):
        """Functions that call to xkcd comics API"""
        if call == 'random':
            comic = xkcd.getRandomComic()
        elif call == 'latest':
            comic = xkcd.getLatestComic()
        elif call.isdigit():
            comic = xkcd.getComic(call)
        else: 
            await ctx.bot.send_message(\
            ctx.message.channel,\
            'Hmm... I can\'t find a comic with that parameter.')
        ctitle = comic.getTitle()
        catext = comic.getAltText()
        curl = comic.getImageLink()
        cimgn = comic.getImageName()
        cnumber = str(comic)[38:]
        # Embed and send message
        embed = discord.Embed(title=ctitle, description=catext)
        embed.set_image(url=curl)
        embed.set_footer(text='xkcd issue {}: {}'.format(cnumber, cimgn))
        await ctx.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def whatIf(self, ctx, call='random'):
        """Functions that call to xkcd whatif API, currently incomplete"""
        if call == 'random':
            whif = xkcd.getRandomWhatIf()
        elif call == 'latest':
            whif = xkcd.getLatestWhatIf()
        elif call.isdigit():
            whif = xkcd.getWhatIf(call)
        else: 
            await ctx.bot.send_message(\
            ctx.message.channel,\
            'Hmm... I can\'t find a WhatIf with that parameter.')
        wtitle = whif.getTitle()
        wurl = whif.getLink()
        wnumber = whif.getNumber()
        # Embed and send message
        embed = discord.Embed(title=wtitle)
        embed.set_image(url=wurl)
        embed.set_footer(text='WhatIf issue {}'.format(wnumber))
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
