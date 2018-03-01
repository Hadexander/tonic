import discord
import urllib.parse
import aiohttp
import asyncio
import re
from lxml import html
from xml.sax.saxutils import unescape
from discord.ext import commands

wikiurl = 'https://pathofexile.gamepedia.com/'
search_limit = 5

def _urlencode(wiki, **kwargs):
    """Forms a request with arbitrary arguments to MediaWiki's api.php, urlencodes special characters.
    Returns: json."""
    kwargs['format'] = 'json'
    return wiki + 'api.php?' + urllib.parse.urlencode(kwargs, quote_via=urllib.parse.quote)

async def wiki_get_item(wiki, name):
    """For a given item name, attempts to retrieve: item infobox, inventory image.
    Returns: dictionary { infobox, image } on success, None on failure."""
    url = _urlencode(wiki, action='cargoquery', tables='items', fields='html, inventory_icon', where="name = '{}'".format(name), limit=1)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if(response.status != 200):
                return None
            json = await response.json()
    json = json.get('cargoquery')
    if not json:
        return None
    json = json[0]
    if not json:
        return None
    json = json.get('title')
    if not json:
        return None
    infobox = json.get('html')
    if not infobox:
        return None
    item = dict()
    item['infobox'] = unescape(infobox)
    icon = json.get('inventory icon')
    if icon:
        image = icon.replace('File:','Special:Filepath/')
    else:
        image = None
    item['image'] = image
    return item

async def wiki_search(wiki, text, limit):
    """Performs a search using the cargotables API. Returns list of possible matches."""
    url = _urlencode(wiki, action='cargoautocomplete', table='items', field='name', substr=text, limit=limit)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if(response.status != 200):
                return None
            json = await response.json()
        items = json.get('cargoautocomplete')
    return items

_links = re.compile(r'\[+|\]+')
_pipes = re.compile(r'\|')

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
        
        item = await wiki_get_item(wikiurl, matches[0])
        if not item:
            await ctx.bot.send_message(ctx.message.channel, 'Could not retrieve item data for "{}"'.format(matches[0]))
            return
        infobox = item['infobox']
        image = item['image']
        tree = html.fromstring(infobox)
        box = infobox_parse(tree)
        
        embed = discord.Embed(title=''.join(box['header']), description=''.join(box['text']))
        if image:
            imageurl = wikiurl + image
            embed.set_thumbnail(url=imageurl)
        alternatives = matches[1:]
        if alternatives:
            #await ctx.bot.send_message(ctx.message.channel, 'Did you mean: {}?'.format(', '.join(alternatives)))
            embed.set_footer(text='Did you mean: {}?'.format(', '.join(alternatives)))
        await ctx.bot.send_message(ctx.message.channel, embed=embed)

