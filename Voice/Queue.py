from Voice.Voice import Voice
from discord.ext import commands

class Queue:
    Voice = Voice()
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
        Queue.Voice.voiceclient.disconnect(ctx)
        
