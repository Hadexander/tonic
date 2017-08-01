import discord
from discord.ext import commands
from storage.lookups import find_user

class VerificationError(commands.CommandError):
    """Exception raised when access level verification fails."""
    pass

async def verify_access_level(uid, level):
    user = await find_user(uid)
    if(user.access < level):
        raise VerificationError(message='Access level violation from {}'.format(uid))

@commands.command(pass_context=True)
async def access(ctx):
    """Tells you your access level."""
    user = await find_user(ctx.message.author.id)
    level = 'user'
    if(user.access > 9000):
        level = 'owner'
    await ctx.bot.send_message(ctx.message.channel, 'You have {} level access with me.'.format(level))
