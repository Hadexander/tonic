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
        Queue.QueueURL.append(yturl)
        return

    @commands.command(pass_context=True)
    async def play(self,ctx,url):
            self._addqueue(url)
            await Queue.Voice.play(Queue.QueueURL[0])
