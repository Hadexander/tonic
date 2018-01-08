import discord
import urllib.parse
import aiohttp
import asyncio
import re
from lxml import html
from discord.ext import commands

wikiurl = 'https://pathofexile.gamepedia.com'
search_limit = 5

def _urlencode(wiki, **kwargs):
    """Forms a request with arbitrary arguments to MediaWiki's api.php, urlencodes special characters.
    Returns: json."""
    kwargs['format'] = 'json'
    return wiki + '/api.php?' + urllib.parse.urlencode(kwargs, quote_via=urllib.parse.quote)

def _jsonpath(json, path):
    """Primitive json traverser, no need for actual JSONPath."""
    i = 0
    while json and i < len(path):
        json = json.get(path[i], [])
        i += 1
    return json

def _smwencode(*args):
    return '|'.join(args)

async def wiki_get_item(session, wiki, name):
    """For a given page on the wiki, attempts to retrieve: tags, item infobox, inventory image.
    Returns: dictionary { infobox, name, tags[], image } on success; None if the page doesn't have the required properties."""
    url = _urlencode(wiki, action='askargs', conditions=_smwencode('Has name::'+name), printouts=_smwencode('Has tags', 'Has infobox HTML', 'Has inventory icon'))
    async with session.get(url) as response:
        if(response.status != 200):
            return None
        json = await response.json()
    json = _jsonpath(json, ['query', 'results', name, 'printouts'])
    if not json:
        return None
    item = dict()
    infobox = json.get('Has infobox HTML')
    if not infobox:
        return None
    item['infobox'] = infobox[0]
    item['name'] = name
    item['tags'] = json.get('Has tags')
    icon = json.get('Has inventory icon')
    if icon:
        image = icon[0].get('fullurl', '').replace('File:','Special:Filepath/')
    else:
        image = ''
    item['image'] = image
    return item

async def wiki_search(wiki, text, limit):
    """Performs a search using the wiki's search engine. For every match found, attempts to retrieve item data.
    Returns: list of 0-limit matched item data."""
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

_links = re.compile('\[+|\]+')
_pipes = re.compile('\|')

def _wikilink_parse(text):
    """Consumes wiki link formatting and returns clean text."""
    subs = _links.split(text)
    return [_pipes.split(s)[-1] for s in subs]

def _format_text(text):
    """Surrounds text with given formatting. Also handles None and empty strings.
    Formatting removed for now."""
    if text:
        return _wikilink_parse(text)
    return []

_header = re.compile('header')
_group = re.compile('group')
_ignore = re.compile('tc -flavour|tc -help')

def infobox_parse(node):
    """Parses the item infobox from an xml tree, recursively, starting at node.
    Returns: dictionary {header[], text[]}; string fragments contained therein need to be joined"""
    dataobj = {'header':[], 'text':[]}
    c = node.get('class')
    if not c:
        #include classless tags?
        dataobj['text'] += _format_text(node.text)
        #handle <br>
        if node.tag == 'br':
            dataobj['text'] += ['\n']
            dataobj['text'] += _format_text(node.tail)
    elif not _ignore.search(c):
        if _header.search(c):
            #header tags
            dataobj['header'] += _format_text(node.text)
        else:
            if _group.search(c):
                #new group
                dataobj['text'] += ['\n']
            #everything else
            dataobj['text'] += _format_text(node.text)
        for child in node:
            co = infobox_parse(child)
            for key in dataobj:
                dataobj[key] += co[key]
        dataobj['text'] += _format_text(node.tail)
    return dataobj

class PathOfExile:
    @commands.command(pass_context=True)
    async def poewiki(self, ctx, *args):
        """Looks up an item on the Path of Exile wiki."""
        itemname = ' '.join(args)
        matches = await wiki_search(wikiurl, itemname, search_limit)
        if not matches:
            await ctx.bot.send_message(ctx.message.channel, 'No item matches "{}"'.format(itemname))
            return
        
        infobox = matches[0]['infobox']
        image = matches[0]['image']
        tree = html.fromstring(infobox)
        box = infobox_parse(tree)
        
        embed = discord.Embed(title=''.join(box['header']), description=''.join(box['text']))
        embed.set_thumbnail(url=image)
        alternatives = [n['name'] for n in matches[1:]]
        if alternatives:
            #await ctx.bot.send_message(ctx.message.channel, 'Did you mean: {}?'.format(', '.join(alternatives)))
            embed.set_footer(text='Did you mean: {}?'.format(', '.join(alternatives)))
        await ctx.bot.send_message(ctx.message.channel, embed=embed)

