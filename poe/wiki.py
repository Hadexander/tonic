import urllib.parse
import aiohttp
import discord
from discord.ext import commands
from lxml import html

def get_printouts(json, item):
    return json['query']['results'][item]['printouts']

def get_imageurl(json):
    return json['Has inventory icon'][0]['fullurl'].replace('File:','Special:Filepath/')

def get_infobox(json):
    return json['Has infobox HTML'][0]

@commands.command(pass_context=True)
async def poewiki(ctx, *args):
    """Looks up an item on the Path of Exile wiki. Case sensitive. No warranty."""
    item = ' '.join(args)
    url = 'https://pathofexile.gamepedia.com/api.php?action=askargs&format=json&conditions=Has%20name::{}&printouts=Has%20infobox%20HTML%7CHas%20inventory%20icon'\
    .format(urllib.parse.quote(item))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if(response.status != 200):
                return
            json = await response.json()
    printouts = get_printouts(json, item)
    imgurl = get_imageurl(printouts)
    infobox = get_infobox(printouts)
    tree = html.fromstring(infobox)
    header = tree.xpath("//span[contains(@class, 'header')]//text()")
    desc = '\n'.join(header[1:])+'\n'
    text = []
    defaults = tree.xpath("//*[contains(@class, '-default')]")
    for d in defaults:
        text.append(''.join(d.xpath("descendant-or-self::*/text()")))
    wraps = tree.xpath("//*[contains(@class, '-textwrap')]")
    for w in wraps:
        text.append('\n'.join(w.xpath("descendant-or-self::*/text()")))
    desc  +=  '\n\n'.join(text)
    desc = desc.replace('[','').replace(']','')
    embed = discord.Embed(title=header[0], description=desc)
    embed.set_thumbnail(url=imgurl)
    await ctx.bot.send_message(ctx.message.channel, embed=embed)
