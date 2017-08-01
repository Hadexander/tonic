import asyncio
import discord
from discord.ext import commands
from storage.lookups import find_user

class VerificationError(commands.CommandError):
    """Exception raised when access level verification fails."""
    pass

def no_private_message(ctx):
    if not ctx.message.server:
        raise commands.NoPrivateMessage()
    return True

def require_owner_access(ctx):
    user = find_user(ctx.message.author.id)
    if not user.access > 9000:
        raise VerificationError(message='Access level violation from {}'.format(ctx.message.author.id))
    return True