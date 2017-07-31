import discord

async def serverwide_prefix(server):
    return '!'

async def command_prefix(bot, message):
    return [bot.user.mention+' ', await serverwide_prefix(message.server)]