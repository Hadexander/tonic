import discord
from discord.ext import commands
from storage.lookups import find_guild
from util.checks import no_private_message

prefix_cache = dict()

async def serverwide_prefix(server):
    if not server:
        return None
    if server not in prefix_cache:
        guild = find_guild(server.id)
        prefix_cache[server.id] = guild.prefix
    return prefix_cache[server.id]

async def command_prefix(bot, message):
    plist = []
    swp = await serverwide_prefix(message.server)
    if(swp):
        plist.extend(swp)
    plist.append(bot.user.mention+' ')
    return plist

@commands.command(pass_context=True)
@commands.check(no_private_message)
async def prefix(ctx, *args):
    """Changes my command prefix string on this server."""
    guild = find_guild(ctx.message.server.id)
    guild.prefix = args
    guild.save()
    if(guild.prefix):
        await ctx.bot.send_message(ctx.message.channel, 'Command prefixes changed to {}'.format(' '.join(guild.prefix)))
    else:
        await ctx.bot.send_message(ctx.message.channel, 'Command prefix disabled. I will still respond to {}'.format(ctx.bot.user.mention))