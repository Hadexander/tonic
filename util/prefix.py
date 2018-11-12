from storage.db import Guild

prefix_cache = dict()

def prefix_changed(gid):
    del prefix_cache[gid]

def command_prefix(bot, message):
    if not message.server:
        return [bot.user.mention+' ', '!']
    gid = message.server.id
    if gid not in prefix_cache:
        guild = bot.database.get(Guild, id=gid)
        prefix_cache[gid] = [bot.user.mention+' ', guild.prefix]
    return prefix_cache[gid]
