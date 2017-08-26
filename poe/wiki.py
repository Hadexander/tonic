import urllib.parse
import aiohttp
import discord
from discord.ext import commands
from lxml import html

wikiurl = 'https://pathofexile.gamepedia.com'
search_limit = 5

def _urlencode(wiki, **kwargs):
    kwargs['format'] = 'json'
    return wiki + '/api.php?' + urllib.parse.urlencode(kwargs, quote_via=urllib.parse.quote)

def _jsonpath(json, path):
    i = 0
    while json and i < len(path):
        json = json.get(path[i], [])
        i += 1
    return json

def _smwencode(*args):
    return '|'.join(args)

async def wiki_get_item(session, wiki, name):
    url = _urlencode(wiki, action='askargs', conditions=_smwencode('Has name::'+name), printouts=_smwencode('Has tags', 'Has infobox HTML', 'Has inventory icon'))
    async with session.get(url) as response:
        if(response.status != 200):
            return None
        json = await response.json()
    json = _jsonpath(json, ['query', 'results', name, 'printouts'])
    if not json:
        return None
    item = dict()
    item['name'] = name
    item['tags'] = json.get('Has tags')
    item['infobox'] = json.get('Has infobox HTML')[0]
    icon = json.get('Has inventory icon')[0]
    item['image'] = icon.get('fullurl', '').replace('File:','Special:Filepath/')
    return item

async def wiki_search(wiki, text, limit):
    url = _urlencode(wiki, action='query', list='search', srsearch=text, srinfo='', srprop='', srlimit=limit)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if(response.status != 200):
                return []
            json = await response.json()
        json = _jsonpath(json, ['query', 'search'])
        results = [r.get('title') for r in json]
        items = []
        for name in results:
            item = await wiki_get_item(session, wiki, name)
            if item:
                items.append(item)
    return items

@commands.command(pass_context=True)
async def poewiki(ctx, *args):
    """Looks up an item on the Path of Exile wiki."""
    itemname = ' '.join(args)
    matches = await wiki_search(wikiurl, itemname, search_limit)
    if not matches:
        await ctx.bot.send_message(ctx.message.channel, 'No item matches "{}"'.format(itemname))
    infobox = matches[0]['infobox']
    image = matches[0]['image']
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
    embed.set_thumbnail(url=image)
    await ctx.bot.send_message(ctx.message.channel, embed=embed)
    alternatives = [n['name'] for n in matches[1:]]
    if alternatives:
        await ctx.bot.send_message(ctx.message.channel, 'Did you mean: {}?'.format(', '.join(alternatives)))
