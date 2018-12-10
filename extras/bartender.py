from discord.ext import commands
from lxml import html
import requests

class Bartender:
    @commands.command(pass_context=True)
    async def orderartist(self,ctx):
        """Ask Tonic for a drink inspired by your favorite artists!"""
        artist = ctx.message.content[6:]
        drink = ""
        response = requests.get('http://drinkify.org/{}'.format(artist))
        if response.status_code == 200:
            root = html.fromstring(response.content)
            recipe = root.xpath('//ul[@class="recipe"]/li/text()')
            for alc in recipe:
                drink +="{}\n".format(alc)
            instructions = root.xpath('normalize-space(//p[@class="instructions"]/text())')
            drink += "\n\nInstructions:\n{}".format(instructions)
        else:
            return
        await ctx.bot.send_message(ctx.message.channel, drink)
