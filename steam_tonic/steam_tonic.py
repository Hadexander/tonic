from steam import SteamClient
from discord.ext import commands
from storage import settings
#Load "config" file.
config = settings.load('Steam')
#Create Steam Client, Login as Bot....
s_tonic = SteamClient()
s_username = config.get('steam_u')
s_password = config.get('steam_p')
s_tonic.cli_login(s_username,s_password)

class Steam_Tonic:
    #Returns Game Dict info
    def _gamesearch_(self,appid):
        #Get Game Info...its a huge file.
        appid = int(appid)
        developer_url = ""
        s_json = s_tonic.get_product_info([appid])
        if "developer_url" in s_json['apps'][appid]['extended']:
            developer_url = s_json['apps'][appid]['extended']['developer_url']
        game = {
        "game": s_json['apps'][appid]['common']['name'],
        "developer": s_json['apps'][appid]['extended']['developer'],
        "publisher": s_json['apps'][appid]['extended']['publisher'],
        "website": developer_url,
        "metascore": s_json['apps'][appid]['common']['metacrtic_score']
        }
        return game

    @commands.command(pass_context=True)
    async def gameinfo(self,ctx,appid):
        game = self._gamesearch_(appid)
        ctx.bot.send_message("Game: ", game['game'],
        "Developer: ", game['developer'],
        "Publisher: ", game['publisher'],
        "Developer Website: ", game['website'],
        "Metacritic Score: ", game['metascore'])
