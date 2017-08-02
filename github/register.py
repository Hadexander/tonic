import discord
from discord.ext import commands
from storage.lookups import find_user

@commands.command(pass_context=True)
async def gitprofile(ctx, name):
    user = find_user(ctx.message.author.id)
    user.github = name
    user.save()