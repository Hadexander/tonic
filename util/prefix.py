import discord
from discord.ext import commands
from storage.lookups import find_guild

prefix_cache = dict()

async def serverwide_prefix(server):
    if not server:
        return None
    if server not in prefix_cache:
        guild = await find_guild(server.id)
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
async def prefix(ctx, *args):
    """Changes my command prefix string on this server."""
    if not ctx.message.server:
        raise commands.NoPrivateMessage()
    guild = await find_guild(ctx.message.server.id)
    guild.prefix = args
    guild.save()
    if(guild.prefix):
        await ctx.bot.send_message(ctx.message.channel, 'Command prefixes changed to {}'.format(' '.join(guild.prefix)))
    else:
        await ctx.bot.send_message(ctx.message.channel, 'Command prefix disabled. I will still respond to {}'.format(ctx.bot.user.mention))