from steam import SteamClient
#from steam import WEBAPI

#Create Steam Client, Login as Bot....
s_tonic = SteamClient()
s_username = config.get('steam_u')
s_password = config.get('steam_p')
s_tonic.cli_login(s_username,s_password)

class Steam:
    #Returns Game Dict info
    def _gamesearch_(self,appid):
        #Get Game Info...its a huge file.
        s_json = s_tonic.get_product_info(appid)
        game = {
        "game": s_json['apps'][107410]['common']['name'],
        "developer": s_json['apps'][107410]['extended']['developer'],
        "publisher": s_json['apps'][107410]['extended']['publisher'],
        "website": s_json['apps'][107410]['extended']['developer_url'],
        "metascore": s_json['apps'][107410]['common']['metacrtic_score']
        }
        return game

    @commands.command(pass_context=True)
    async def gameinfo(self,ctx):
        game = self._gamesearch_(ctx.message.content)
        ctx.bot.send_message("\`\`\`
        Game: ", game['game'],
        "Developer: ", game['developer'],
        "Publisher: ", game['publisher'],
        "Developer Website: ", game['website'],
        "Metacritic Score: ", game['metascore'],"
        \`\`\`")
