import math
import aiohttp
import discord
from discord.ext import commands
from extras.imgur import image_upload, image_delete
from storage.db import Emoji as EmojiObj
from storage.db import Guild
from util.checks import no_private_message

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
    embed.set_image(url=emoji.url)
    embed.set_footer(text=emoji.name)
    return embed


class Emoji:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database
    
    @commands.command(pass_context=True)
    @commands.check(no_private_message)
    async def emsave(self, ctx, name, url=None):
        """Saves an emoji to my gallery. Can be a URL or direct attachment. Or you could just use this command right after an image is posted."""
        # check if emoji exists
        e = self.db.get(EmojiObj, guild=ctx.message.server.id, name=name)
        if e:
            await ctx.bot.send_message(ctx.message.channel, '{} already exists'.format(name))
            return
        # attempt to find a valid image url
        try:
            if not url:
                # if url argument is missing, check attachments and message history
                if ctx.message.attachments:
                    url = ctx.message.attachments[0]['url']
                else:
                    async for log in ctx.bot.logs_from(ctx.message.channel, limit=1, before=ctx.message):
                        if log.attachments:
                            url = log.attachments[0]['url']
                        else:
                            url = log.content
            await _validate_url_image(url)
        except (TypeError, ValueError, discord.Forbidden, discord.NotFound, discord.HTTPException):
            await ctx.bot.send_message(ctx.message.channel, 'No valid image found.')
            return
        # upload image if found
        data = await image_upload(url)
        if 'error' in data:
            await ctx.bot.send_message(ctx.message.channel, '{}. Gallery copy failed: {}'.format(name, data['error']))
        else:
            e = EmojiObj(guild=ctx.message.server.id, name=name, url=data['link'])
            self.db.add(e)
            self.db.commit()
            await ctx.bot.send_message(ctx.message.channel, 'Saved {}.'.format(name))

    @commands.command(pass_context=True)
    @commands.check(no_private_message)
    async def em(self, ctx, name):
        """Repost an emoji from my gallery."""
        e = self.db.get(EmojiObj, guild=ctx.message.server.id, name=name)
        if e:
            await ctx.bot.send_message(ctx.message.channel, embed=_emoji_embed(e))

    @commands.command(pass_context=True)
    @commands.check(no_private_message)
    async def emdelete(self, ctx, name):
        """Removes an emoji from my gallery."""
        e = self.db.get(EmojiObj, guild=ctx.message.server.id, name=name)
        self.db.delete(e)
        self.db.commit()
        await ctx.bot.send_message(ctx.message.channel, "Deleted {}".format(name))

    @commands.command(pass_context=True)
    @commands.check(no_private_message)
    async def emlist(self, ctx):
        """Lists all emojis from my gallery."""
        emojis = self.db.getall(EmojiObj, guild_id=ctx.message.server.id)
        e = []
        for n in emojis:
            e.append(n.name)
        e.sort()

        max_e = len(e)
        row_e = int(math.ceil(max_e / 3))

        e1 = e[:row_e]
        e2 = e[row_e:row_e*2]
        e3 = e[row_e*2:]

        row1 = ""
        row2 = ""
        row3 = ""

        for x in e1:
            row1 += "\n"+x

        for x in e2:
            row2 += "\n"+x

        for x in e3:
            row3 += "\n"+x

        H1 = (e1[0][0] + " - " + e1[len(e1)-1][0]).upper()
        H2 = (e2[0][0] + " - " + e2[len(e2)-1][0]).upper()
        H3 = (e3[0][0] + " - " + e3[len(e3)-1][0]).upper()

        embed = discord.Embed()

        embed.add_field(name=H1, value=row1, inline=True)
        embed.add_field(name=H2, value=row2, inline=True)
        embed.add_field(name=H3, value=row3, inline=True)

        await ctx.bot.send_message(ctx.message.channel, embed=embed)
