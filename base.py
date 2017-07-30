import discord
import asyncio
import sys
import time
import socket
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #hard-coding ids should be avoided
    #the bot needs to store a list of channels you want to notify at startup
    #on_ready may be called multiple times, need a better way to notify only once per startup
    #await client.send_message(client.get_channel('133578549432025088'),'Im up and running! :smiley: \n \n' + 'My current time is: ' + time.asctime() + '\n \n' + 'and Im running from: ' + socket.gethostname() )
    
@client.event
async def on_message(message):
    #ignore messages from self and other bots
    if(message.author.bot):
        return
    #figure out if message is a command for me
    command = await extract_command(message.content)
    #split into argument list
    args = command.split()
    if(len(args) > 0):
        #find respective coroutine
        coroutine = commands.get(args[0], None)
        if(coroutine is not None):
            await coroutine(message, args)

async def extract_command(text):
    text = text.strip()
    if(text.startswith(prefix)):
        return text.lstrip(prefix)
    elif(text.startswith(client.user.mention)):
        text = text.replace(client.user.mention, '')
        return text.strip()
    else:
        return ''

async def test(message, *args):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=100):
        if log.author == message.author:
            counter += 1
    await client.edit_message(tmp, 'You have {} messages.'.format(counter))

async def sleep(message, *args):
    await asyncio.sleep(5)
    await client.send_message(message.channel, 'Done sleeping')

async def cmd_lp(message, *args):
    await client.send_message(message.channel, 'Let\'s play!', tts = True)

async def emtest(message, *args):
    em = discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDEADBF)
    em.set_author(name='Someone', icon_url=client.user.default_avatar_url)
    await client.send_message(message.channel, embed=em)

async def upgrade(message, *args):
    tmp = await client.send_message(message.channel, 'OK! \n\
    Upgrading my systems...')
    with open('avi.png', 'rb') as avi:
        await client.edit_profile(avatar=avi.read())
    await client.edit_message(tmp, \
    'OK!\n \
    Upgrading my systems...\n \
    Systems upgraded, I have a new face!')

prefix = '!'
commands = {
    'test' : test,
    'sleep' : sleep,
    'lp' :  cmd_lp,
    'emtest' : emtest,
    'upgrade' : upgrade
}
client.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')