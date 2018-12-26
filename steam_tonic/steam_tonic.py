from discord.ext import commands
from lxml import html
import discord
import requests
import json


class Steam_Tonic:


    def __gamesearch__(self,game):
        #Uses steam's search engine.
        response = requests.get('https://store.steampowered.com/search/?term={}'.format(game)).content
        root = html.fromstring(response)
        #parse through results and get the first element of results.
        newroot = root.xpath('//a[@class= "search_result_row ds_collapse_flag " ]')
        if newroot is None or len(newroot) < 1:
            return False
        appid = newroot[0].get('data-ds-appid')
        return appid

    def __isMedia__(self,game_res,appid):
        mediatype = game_res[appid]['data']['type']
        if mediatype == 'movie' or mediatype == 'series':
            return True
        return False

    def __getPrice__(self,game_res,appid):
        if  game_res[appid]['data']['is_free']:
            return "Free!"
        elif 'price_overview' in game_res[appid]['data'] :
            return game_res[appid]['data']['price_overview']['final_formatted']
        else:
            return "TBA"
        return False

    def __getReleaseDate__(self,game_res,appid):
        if game_res[appid]['data']['release_date']['coming_soon']:
            date = "Coming soon in: {}".format(game_res[appid]['data']['release_date']['date'])
        else:
            date = "Released on: {}".format(game_res[appid]['data']['release_date']['date'])
        return date

    def __getGenres__(self,game_res,appid):
        genrelist = game_res[appid]['data']['genres']
        genres = ""
        for genre in genrelist:
            genres+="{}, ".format(genre['description'])
        return genres

    def __getDescription__(self,game_res,appid):
        description = game_res[appid]['data']['short_description']
        return description

    def __getGameName__(self,game_res,appid):
        g_name = game_res[appid]['data']['name']
        return g_name

    def __getDevelopers__(self,game_res,appid):
        developerslist = game_res[appid]['data']['developers']
        developers= ""
        if len(developerslist) < 2:
            return developerslist[0]
        else:
            for Pub in developerslist:
                developers += "{},".format(Pub)
        return developers

    def __getPublisher__(self,game_res,appid):
        publisher = game_res[appid]['data']['publishers'][0]
        return publisher

    def __getMetascore__(self,game_res,appid):
        if 'metacritic' in game_res[appid]['data']:
            metacritic_score = game_res[appid]['data']['metacritic']['score']
            return metacritic_score
        else:
            return "N/A"
        return

    @commands.command(pass_context=True)
    async def gameinfo(self,ctx):
        """Searches a game on steam"""
        #Calls api for appid (will later be provided by an internal DB)
        game = ctx.message.content[9:]
        appid = self.__gamesearch__(game)
        #check if we even got a result
        if not appid:
            await ctx.bot.send_message(ctx.message.channel, "Game not found")
            return
        response = json.loads(requests.get('https://store.steampowered.com/api/appdetails?appids=%s' %appid).content)
        #Checks if there was a valid response
        if response is None or 'data' not in response[appid]:
            await ctx.bot.send_message(ctx.message.channel, "Game not found")
            return
        #getters
        g_name = self.__getGameName__(response,appid)
        developers = self.__getDevelopers__(response,appid)
        publisher = self.__getPublisher__(response,appid)
        description = self.__getDescription__(response,appid)
        genres = self.__getGenres__(response,appid)
        price = self.__getPrice__(response,appid)
        metascore = self.__getMetascore__(response,appid)
        date = self.__getReleaseDate__(response,appid)
        #Build out string for embed
        message = """ **Game:** {} \n **Developer:** {} \n **Publisher:** {} \n\n\n **Description** \n{} \n \n \n **Genres:** {} \n *{}* \n**Price(EUR):** *{}*
        **Metacritic Score:** {} """.format(
        g_name,
        developers,
        publisher,
        description,
        genres,
        date,
        price,
        metascore)
        #Create embeding
        finalout = discord.Embed(title=g_name,description=message,url = 'https://store.steampowered.com/app/%s' %appid)
        finalout.set_image(url=response[appid]['data']['header_image'])
        finalout.set_author(name="Steam",url='https://store.steampowered.com')
        await ctx.bot.send_message(ctx.message.channel, embed=finalout)
        return
