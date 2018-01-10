import aiohttp
import discord
from discord.ext import commands
from extras.imgur import image_upload, image_delete
from storage.lookups import find_emoji

async def _get_content_type(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            return response.headers.get('content-type')

async def _validate_url_image(url):
    ctype = await _get_content_type(url)
    if(not ctype or not (ctype.startswith('image') or ctype.startswith('video'))):
        raise ValueError

def _emoji_embed(emoji):
    embed = discord.Embed()
    ctype = await _get_content_type(emoji.url)
    if(ctype.startswith('image')):
        embed.set_image(url = emoji.url)
    else:
        embed.description = emoji.url
    embed.set_footer(text = emoji.name)
    return embed

class Emoji:
    @commands.command(pass_context=True)
    async def emsave(self, ctx, name, url=None):
        """Saves an emoji to my gallery. Can be a URL or direct attachment. Or you could just use this command right after an image is posted."""
        e = find_emoji(name)
        if(e.name):
            await ctx.bot.send_message(ctx.message.channel, 'I already have \'{}\', use a different name or !emdelete.'.format(name))
            return
        e.name = name
        try:
            if(not url):
                if(ctx.message.attachments):
                    url = ctx.message.attachments[0]['url']
                else:
                    async for log in ctx.bot.logs_from(ctx.message.channel, limit=1, before=ctx.message):
                        if(log.attachments):
                            url = log.attachments[0]['url']
                        else:
                            url = log.content
            await _validate_url_image(url)
        except(TypeError, ValueError, discord.Forbidden, discord.NotFound, discord.HTTPException):
            await ctx.bot.send_message(ctx.message.channel, 'No valid image found.')
            return
        data = await image_upload(url)
        if('error' in data):
            e.url = url
            await ctx.bot.send_message(ctx.message.channel, 'Saved {}. Gallery copy failed: {}'.format(name, data['error']))
        else:
            e.url = data['link']
            e.id = data['id']
            await ctx.bot.send_message(ctx.message.channel, 'Saved {}.'.format(name))
        e.save()
    
    @commands.command(pass_context=True)
    async def em(self, ctx, name):
        """Repost an emoji from my gallery."""
        e = find_emoji(name)
        if(e.url):
            await ctx.bot.send_message(ctx.message.channel, embed = _emoji_embed(e))

    @commands.command(pass_context=True)
    async def emdelete(self, ctx, name):
        """Removes an emoji from my gallery."""
        e = find_emoji(name)
        if(e.url):
            if(e.id):
                await image_delete(e.id)
            e.remove()
            await ctx.bot.send_message(ctx.message.channel, 'Deleted '+name)
