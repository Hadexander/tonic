from discord.ext import commands, client
import asyncio, pickle
import numpy as np

def readPickle(shitIn='lexicon.pkl'):
    with open(shitIn, 'rb') as pickleFile:
        lexicon = pickle.load(pickleFile)
    return lexicon

lexicon = readPickle()

async def talkSmack(firstWord, length):
    firstWord = firstWord
    chain = [firstWord]
    chain_len = length

    for i in range(chain_len):
        chain.append(np.random.choice(lexicon[chain[-1]]))

    smack = ' '.join(chain)
    return smack

class Friendbot:

    @commands.command(pass_context=True)
    async def talk(self, ctx, word):
        reply = await talkSmack(word, 30)
        await client.send_message(ctx.message.channel, reply)

    @commands.command(pass_context=True)    
    async def rant(self, ctx, word):
        reply = await talkSmack(word, 90)
        await client.send_message(ctx.message.channel, reply)
