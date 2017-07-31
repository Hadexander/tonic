import discord
from discord.ext import commands
import aiohttp
import imghdr
from util.verification import verify_access_level

@commands.command(pass_context=True)
async def avatar(ctx, url):
    """Changes my avatar from a URL."""
    await verify_access_level(ctx.message.author.id, 9000)
    if(not url):
        return
    msg = await ctx.bot.send_message(ctx.message.channel, 'Downloading new avatar...')
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if(response.status == 200):
                    avi = await response.read()
                    if(imghdr.what('', h = avi)):
                        await ctx.bot.edit_profile(avatar = avi)
                        await ctx.bot.edit_message(msg, 'Avatar changed.')
                    else:
                        await ctx.bot.edit_message(msg, 'I\'m sorry, that\'s not a valid image')
                else:
                    await ctx.bot.edit_message(msg, 'I\'m sorry, download failed: %s' %(response.reason))
        except ValueError:
            await ctx.bot.edit_message(msg, "I\'m sorry, the URL was invalid.")