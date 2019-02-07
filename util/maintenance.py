import imghdr
import aiohttp
import asyncio
import shlex
import logging
from discord.ext import commands
from storage.db import User, Guild
from .checks import require_owner_access, no_private_message, require_server_permissions
from .prefix import prefix_changed
from .logger import DiscordLoggingHandler, DiscordLoggingFormatter

log_levels = {
    "DEBUG":10,
    "INFO":20,
    "WARNING":30,
    "ERROR":40,
    "CRITICAL":50}

class Maintenance:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database
        self.loggers = {}
    
    @commands.command(pass_context=True)
    async def access(self, ctx):
        """Tells you your access level."""
        user = self.db.get(User, id=ctx.message.author.id)
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
    async def dev(self, ctx, command, param=None):
        """Developer commands.
        branch - find out which branch I'm on
        evolve - get updates from current branch and restart
        evolve <branch_name> - change to a different branch, update and restart
        log <level> - start/stop logging to the current channel with specified python logging level"""
        if command == 'branch':
            shell = await asyncio.create_subprocess_shell("git rev-parse --abbrev-ref HEAD", stdout=asyncio.subprocess.PIPE)
            stdout, stderr = await shell.communicate()
            bname = stdout.decode().strip()
            await ctx.bot.send_message(ctx.message.channel, "Current branch: {}".format(bname))
        elif command == 'evolve':
            msg = "Grabbing the latest updates."
            if param:
                shell = await asyncio.create_subprocess_shell("git fetch")
                await shell.wait()
                shell = await asyncio.create_subprocess_shell("git checkout {}".format(shlex.quote(param)))
                code = await shell.wait()
                if code != 0:
                    await ctx.bot.send_message(ctx.message.channel, "Couldn't change to branch: {}".format(param))
                    return
                else:
                    msg = "Changed to branch: {}. {}".format(param, msg)
            await ctx.bot.send_message(ctx.message.channel, msg)
            await ctx.bot.close()
        elif command == 'log':
            cname = ctx.message.channel.name
            logger = logging.getLogger()
            if cname in self.loggers:
                self.loggers[cname].close()
                logger.removeHandler(self.loggers[cname])
                del self.loggers[cname]
                await ctx.bot.send_message(ctx.message.channel, "Logging stopped.")
            else:
                if param not in log_levels:
                    await ctx.bot.send_message(ctx.message.channel, "Specify logging level: CRITICAL, ERROR, WARNING, INFO, DEBUG")
                    return
                level = log_levels[param]
                handler = DiscordLoggingHandler(ctx.bot, ctx.message.channel)
                handler.setLevel(level)
                handler.setFormatter(DiscordLoggingFormatter())
                logger.addHandler(handler)
                self.loggers[cname] = handler
                await ctx.bot.send_message(ctx.message.channel, "Logging started.")
        else:
            raise commands.MissingRequiredArgument()
    
    @commands.command(pass_context=True)
    @commands.check(no_private_message)
    @commands.check(require_server_permissions)
    async def prefix(self, ctx, string=None):
        """Changes my command prefix string on this server."""
        guild_id = ctx.message.server.id
        guild = self.db.get(Guild, id=guild_id)
        guild.prefix = string
        prefix_changed(guild_id)
        self.db.commit()
        if(guild.prefix):
            await ctx.bot.send_message(ctx.message.channel, f"Command prefix changed to {guild.prefix}")
        else:
            await ctx.bot.send_message(ctx.message.channel, f"Command prefix disabled. I will still respond to {ctx.bot.user.mention}")
    