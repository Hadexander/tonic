import re
import aiohttp
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from lxml import etree
from io import BytesIO
from storage.lookups import find_user

github_font = ImageFont.truetype('segoeui.ttf', size=12)

def get_size(root):
    return (int(root.get('width')), int(root.get('height')))

def parse(node, image, position=(0,0)):
    if node.tag == 'g':
        delta = translate(node)
        position = add(position, delta)
    elif node.tag == 'rect':
        rect(node, image, position)
    elif node.tag == 'text':
        text(node, image, position)
    for child in node:
        parse(child, image, position)

def translate(node):
    tf = node.get('transform', '')
    return tuple(int(x) for x in re.findall(r'\d+', tf))

def add(a, b):
    return tuple(map(sum, zip(a, b)))

def rect(node, image, position):
    w = int(node.get('width'))
    h = int(node.get('height'))
    x = int(node.get('x')) + position[0]
    y = int(node.get('y')) + position[1]
    r = [x, y, x+w, y+h]
    fill = node.get('fill', '')
    image.rectangle(r, fill)

def text(node, image, position):
    c = node.get('class')
    if c == 'month':
        x = int(node.get('x')) + position[0]
        y = int(node.get('y')) + position[1] - 10
    elif c == 'wday':
        if node.get('style') == "display: none;":
            return
        x = int(node.get('dx')) + position[0]
        y = int(node.get('dy')) + position[1] - 10
    image.text((x, y), node.text, '#767676', github_font)

@commands.command(pass_context=True)
async def mygit(ctx):
    user = find_user(ctx.message.author.id)
    if not user.github:
        await ctx.bot.send_message(ctx.message.channel, 'You need to register your github profile first.')
        return
    name = user.github
    url = 'https://github.com/users/{}/contributions'.format(name)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if(response.status != 200):
                return
            svg = await response.read()
    root = etree.fromstring(svg)
    with Image.new(mode='RGB', size = get_size(root), color='#ffffff') as img:
        draw = ImageDraw.Draw(img)
        parse(root, draw)
        with BytesIO() as output:
            img.save(output, 'PNG')
            output.seek(0)
            msg = await ctx.bot.send_file(ctx.message.channel, fp=output, filename='contributions.png')
    await embed_mygit(ctx, msg, name)

async def embed_mygit(ctx, message, name):
    disname = ctx.message.author.name
    if isinstance(ctx.message.author, discord.Member):
        if(ctx.message.author.nick):
            disname = ctx.message.author.nick
    title = '{} ({})'.format(disname, name)
    giturl = 'https://github.com/{}'.format(name)
    image = message.attachments[0]
    embed = discord.Embed(title=title, url=giturl, colour=discord.Colour.green(), timestamp=message.timestamp)
    embed.set_image(url=image['url'])
    await ctx.bot.send_message(ctx.message.channel, embed=embed)
    await ctx.bot.delete_message(message)