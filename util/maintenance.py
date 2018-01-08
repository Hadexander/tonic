import imghdr
import aiohttp
from discord.ext import commands
from storage.lookups import find_user
from util.checks import require_owner_access

class Maintenance:
    @commands.command(pass_context=True)
    async def access(self, ctx):
        """Tells you your access level."""
        user = find_user(ctx.message.author.id)
        level = 'user'
        if(user.access > 9000):
            level = 'owner'
        await ctx.bot.send_message(ctx.message.channel, 'You have {} level access with me.'.format(level))

    @commands.command(pass_context=True)
    @commands.check(require_owner_access)
    async def avatar(self, ctx, url):
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
    @commands.check(require_owner_access)
    async def evolve(self, ctx):
        """Orders me to restart and update from git."""
        msg = 'Getting some improvements! I\'ll be back as soon as possible!'
        await ctx.bot.send_message(ctx.message.channel, msg)
        await ctx.bot.close()
