import discord
from discord.ext import commands
from storage.lookups import retrieve_user

class VerificationError(commands.CommandError):
    """Exception raised when access level verification fails."""
    pass

async def verify_access_level(uid, level):
    user = await retrieve_user(uid)
    if(user.access < level):
        raise VerificationError(message='Access level violation from %s' %(uid))

@commands.command(pass_context=True)
async def access(ctx):
    """Tells you your access level."""
    user = await retrieve_user(ctx.message.author.id)
    level = 'user'
    if(user.access > 9000):
        level = 'owner'
    await ctx.bot.send_message(ctx.message.channel, 'You have %s level access with me.' % (level))