import discord
import asyncio
import sys
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):   
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith('!lp'):
        await client.send_message(message.channel, 'Let\'s play!', tts = True)

    if message.content.startswith('!emtest'):
        em = discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDEADBF)
        em.set_author(name='Someone', icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel, embed=em)
    
    if message.content.startswith('!upgrade'):
        tmp = await client.send_message(message.channel, 'OK! \n\
        Upgrading my systems...')
        with open('avi.png', 'rb') as avi:
            await client.edit_profile(avatar=avi.read())
        await client.edit_message(tmp, \
        'OK!\n \
        Upgrading my systems...\n \
        Systems upgraded, I have a new face!')

client.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')