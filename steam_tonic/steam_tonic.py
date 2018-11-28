from discord.ext import commands
from storage import settings
import discord
import requests
import json

class Steam_Tonic:

    @commands.command(pass_context=True)
    async def gameinfo(self,ctx,appid):
        #Calls api for appid (will later be provided by an internal DB)
        response = json.loads(requests.get('https://store.steampowered.com/api/appdetails?appids=%s' %appid).content)
        #Checks if there was a valid response
        if response is None or 'data' not in response[appid]:
            await ctx.bot.send_message(ctx.message.channel, "Game not found")
            return
        if response[appid]['data']['type'] == 'movie':
            return
        #Builds data from response
        message = "Game: {} \n Developer: {} \n Publisher: {} \n Description: {} \n Price(USD): {}".format(
        response[appid]['data']['name'],
        response[appid]['data']['developers'][0],
        response[appid]['data']['publishers'][0],
        response[appid]['data']['short_description'],
        response[appid]['data']['price_overview']['final_formatted'])
        image = discord.Embed()
        image.set_image(url=response[appid]['data']['header_image'])
        image.set_footer(text='https://store.steampowered.com/app/%s'%appid)
        await ctx.bot.send_message(ctx.message.channel, embed=image)
        await ctx.bot.send_message(ctx.message.channel,'```%s```'%message)
        return
