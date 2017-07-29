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

    elif message.content.startswith('!die'):
        await client.send_message(message.channel, 'Ima go die now..')
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'dead in 3..')
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'dead in 2..')
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'dead in 1..')
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'RIP')
        sys.exit(0)

client.run('MzQwOTE5NDIxMjQzNjIxMzc3.DF5kGQ.gz23fwEWEb8UrQCzoSRXUvrnOyY')