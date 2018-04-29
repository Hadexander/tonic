import aiohttp
import discord
from discord.ext import commands
from extras.imgur import image_upload, image_delete
from storage.lookups import find_emoji, save_emoji, delete_emoji

async def _get_content_type(url):
    """Checks page header and returns MIME content type."""
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            return response.headers.get('content-type')

async def _validate_url_image(url):
    """Raises ValueError for unsupported content types."""
    ctype = await _get_content_type(url)
    if(not ctype or not (ctype.startswith('image') or ctype.startswith('video'))):
        raise ValueError

def _emoji_embed(emoji):
    """Generates a discord embed for an image."""
    embed = discord.Embed()
    embed.set_image(url = emoji[0])
    embed.set_footer(text = emoji[1])
    return embed

class Emoji:
    @commands.command(pass_context=True)
    async def emsave(self, ctx, name, url=None):
        """Saves an emoji to my gallery. Can be a URL or direct attachment. Or you could just use this command right after an image is posted."""
        
        #attempt to find a valid image url
        try:
            if(not url):
                #if url argument is missing, check attachments and message history
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
        #upload image if found
        data = await image_upload(url)
        if('error' in data):
            await ctx.bot.send_message(ctx.message.channel, '{}. Gallery copy failed: {}'.format(name, data['error']))
        else:
            e = save_emoji(name,data['link'])
            if(e == name):
                await ctx.bot.send_message(ctx.message.channel, 'Saved {}.'.format(name))
            else:
                await ctx.bot.send_message(ctx.message.channel, e)
        
    
    @commands.command(pass_context=True)
    async def em(self, ctx, name):
        """Repost an emoji from my gallery."""
        e = find_emoji(name)
        if(e):
            try:
                arr = [e,name]
                await ctx.bot.send_message(ctx.message.channel, embed = _emoji_embed(arr))
            except:
                await ctx.bot.send_message(ctx.message.channel, e)

    @commands.command(pass_context=True)
    async def emdelete(self, ctx, name):
        """Removes an emoji from my gallery."""
        e = delete_emoji(name)
        await ctx.bot.send_message(ctx.message.channel, e)
