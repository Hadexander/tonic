import discord
from discord.ext import commands
import aiohttp
import imghdr
from storage.lookups import find_user
from util.checks import require_owner_access

@commands.command(pass_context=True)
async def access(ctx):
    """Tells you your access level."""
    user = find_user(ctx.message.author.id)
    level = 'user'
    if(user.access > 9000):
        level = 'owner'
    await ctx.bot.send_message(ctx.message.channel, 'You have {} level access with me.'.format(level))

@commands.command(pass_context=True)
@commands.check(require_owner_access)
async def avatar(ctx, url):
    """Changes my avatar from a URL."""
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
                    await ctx.bot.edit_message(msg, 'I\'m sorry, download failed: {}'.format(response.reason))
        except ValueError:
            await ctx.bot.edit_message(msg, "I\'m sorry, the URL was invalid.")

@commands.command(pass_context=True)
async def evolve(ctx):
    """Exits Tonic in order for Gin to git pull and relaunch"""
    msg = 'Getting some improvements! I\'ll be back in a sec!'
    await ctx.bot.send_message(ctx.message.channel, msg)
    await ctx.bot.close()
