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
        metacritic_score = "None"
        genres = ""
        #Checks if there was a valid response
        if response is None or 'data' not in response[appid]:
            await ctx.bot.send_message(ctx.message.channel, "Game not found")
            return
        #checks if its a movie as we're not interested in those.
        if response[appid]['data']['type'] == 'movie':
            return
        #Is the game free?
        if  response[appid]['data']['is_free']:
            price = "Free!"
        elif 'price_overview' in response[appid]['data'] :
            price = response[appid]['data']['price_overview']['final_formatted']
        else:
            price = "TBA"
        #Check if game is released or not.
        if response[appid]['data']['release_date']['coming_soon']:
            date = "Coming soon in: {}".format(response[appid]['data']['release_date']['date'])
        else:
            date = "Released on: {}".format(response[appid]['data']['release_date']['date'])
            #Check if there's a metacritic score Also
            if 'metacritic' in response[appid]['data']:
                metacritic_score = response[appid]['data']['metacritic']['score']
                metacritic_url = response[appid]['data']['metacritic']['url']
        #Build Genre table
        for genre in response[appid]['data']['genres']:
            genres+="{}, ".format(genre['description'])
        #Builds data from response
        g_name = response[appid]['data']['name']
        message = """ **Game:** {} \n **Developer:** {} \n **Publisher:** {} \n\n\n **Description** \n{} \n \n \n **Genres:** {} \n *{}*   Price(EUR): *{}*
        **Metacritic Score:** {} """.format(
        g_name,
        response[appid]['data']['developers'][0],
        response[appid]['data']['publishers'][0],
        response[appid]['data']['short_description'],
        genres,
        date,
        price,
        metacritic_score)
        #Builds embeding based off everything we compiled together
        finalout = discord.Embed(title=g_name,description=message,url = 'https://store.steampowered.com/app/%s' %appid)
        finalout.set_image(url=response[appid]['data']['header_image'])
        finalout.set_author(name="Steam",url='https://store.steampowered.com')
        await ctx.bot.send_message(ctx.message.channel, embed=finalout)
        return
