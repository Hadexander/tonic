from Voice.Voice import Voice
from discord.ext import commands

class Queue:
    Voice = Voice()
    QueueURL=[]
    @commands.command(pass_context=True)
    async def join(self,ctx):
        """Bot joins current user's channel"""
        if Voice.voiceclient is None:
            await Queue.Voice.join(ctx)
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m already here')
            return

    @commands.command(pass_context=True)
    async def disconnect(self,ctx):
        """Disconnects from current channel"""
        await Queue.Voice.disconnect(ctx)
        return

    def _addqueue(self,yturl):
        """Adds url to a queue list in case a song is already playing"""
        Queue.QueueURL.append(yturl)
        return

    def _removequeue(self):
        """Removes first item in queue list"""
        Queue.QueueURL.pop(0)
        return
    @commands.command(pass_context=True)
    async def clear(self,ctx):
        """Clears entire queue. Becareful!"""
        Queue.QueueURL.clear()
        await ctx.bot.send_message(ctx.message.channel, 'Music queue empty. Like this bottle of Gin.')
        return

    @commands.command(pass_context=True)
    async def queue(self,ctx):
        """Shows current queued items"""
        await ctx.bot.send_message(ctx.message.channel, "We have about {} songs in queue".format(len(Queue.QueueURL)) )
        await ctx.bot.send_message(ctx.message.channel, Queue.QueueURL)

    @commands.command(pass_context=True)
    async def play(self,ctx,url):
        """Plays youtube links. IE 'https://www.youtube.com/watch?v=mPMC3GYpBHg' """
        if Queue.Voice.voiceclient is None:
            self._addqueue(url)
            await Queue.Voice.play(ctx,Queue.QueueURL[0])
            self._removequeue()
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing something but I'll add it to the queue!")
            self._addqueue(url)
            return

    @commands.command(pass_context=True)
    async def next(self,ctx):
        """Plays song next in queue."""
        if Queue.Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m not even in a channel. :thonking:')
            return
        elif Queue.Voice.player is None:
            await Queue.Voice.play(ctx,Queue.QueueURL[0])
            self._removequeue()
            return
        else:
            await Queue.Voice.stop(ctx)
            await Queue.Voice.play(ctx,Queue.QueueURL[0])
            self._removequeue()
            await ctx.bot.send_message(ctx.message.channel, 'Here we go skipping again!')
            return

    @commands.command(pass_context=True)
    async def pause(self,ctx):
        """Pauses song"""
        await Queue.Voice.pause(ctx)
        return

    @commands.command(pass_context=True)
    async def stop(self,ctx):
        """Stops playback"""
        await Queue.Voice.stop(ctx)
        return

    @commands.command(pass_context=True)
    async def resume(self,ctx):
        """Resumes playback"""
        await Queue.Voice.resume(ctx)
        return

    @commands.command(pass_context=True)
    async def setvolume(self,ctx, vol):
        """Sets volume between 0 and 200."""
        vol = int(vol)
        await Queue.Voice.setvolume(ctx,vol)
        return
