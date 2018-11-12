import asyncio
import discord
from discord.ext import commands
from storage.db import User

class VerificationError(commands.CommandError):
    """Exception raised when access level verification fails."""
    pass

def no_private_message(ctx):
    if not ctx.message.server:
        raise commands.NoPrivateMessage()
    return True

def require_owner_access(ctx):
    user = ctx.bot.database.get(User, id=ctx.message.author.id)
    if not user.access > 9000:
        raise VerificationError(message='Access level violation from {}'.format(ctx.message.author.id))
    return True

def require_server_permissions(ctx):
    if not isinstance(ctx.message.author, discord.Member):
        raise commands.NoPrivateMessage()
    if not ctx.message.author.server_permissions.manage_server:
        raise VerificationError(message='User has insufficient server permissions.')
    return True