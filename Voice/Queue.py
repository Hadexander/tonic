from Voice.Voice import Voice
from discord.ext import commands

class Queue:
    Voice = Voice()
    @commands.command(pass_context=True)
    async def join(self,ctx):
        if Voice.voiceclient is None:
            await Voice.join(ctx)
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m already here')
            return
