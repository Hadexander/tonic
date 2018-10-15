from Voice.Voice import Voice
from discord.ext import commands

class Queue:
    Voice = Voice()
    QueueURL=[]
    @commands.command(pass_context=True)
    async def join(self,ctx):
        if Voice.voiceclient is None:
            await Queue.Voice.join(ctx)
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m already here')
            return

    @commands.command(pass_context=True)
    async def disconnect(self,ctx):
        await Queue.Voice.disconnect(ctx)

    def _addqueue(self,yturl):
        Queue.QueueURL.insert(0,yturl)
        return

    def _removequeue(self):
        Queue.QueueURL.pop(0)
        return
    @commands.command(pass_context=True)
    async def clear(self,ctx,url):
        Queue.QueueURL.clear()

    @commands.command(pass_context=True)
    async def play(self,ctx,url):
        if Queue.Voice.voiceclient is None:
            self._addqueue(url)
            await Queue.Voice.play(ctx,Queue.QueueURL[0])
            self._removequeue()
            return
        else:
            self._addqueue()
            return

    @commands.command(pass_context=True)
    async def next(self,ctx,url):
        if Queue.Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m not even in a channel. :thonking:')
        if Queue.Voice.player is None:
            await Queue.Voice.play(ctx,Queue.QueueURL[0])
        else:
            await Queue.Voice.stop(ctx)
            await Queue.Voice.play(ctx,Queue.QueueURL[0])
            await ctx.bot.send_message(ctx.message.channel, 'Here we go skipping again!')
