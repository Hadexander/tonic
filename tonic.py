import shelve
import asyncio
import discord
from discord.ext.commands import *

async def command_prefix(me : Bot, message : discord.Message):
    return [bot.user.mention+' ', '!']

db = shelve.open('storage')
owner_ids = db.get('owners', [])
owner_users = []
bot = Bot(command_prefix)

@bot.event
async def on_ready():
    print('Logged in ('+bot.user.name+':'+bot.user.id+')')
    for id in owner_ids:
        user = await bot.get_user_info(id)
        owner_users.append(user)
        await bot.send_message(user, 'I am online, master.')

@bot.command(pass_context=True)
async def owners(ctx):
    """List users with admin level access."""
    ustr = []
    for user in owner_users:
        ustr.append(str(user))
    msg = '\n'.join(ustr)
    await bot.send_message(ctx.message.channel, 'My owners are:\n'+msg)

bot.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')
db.close()