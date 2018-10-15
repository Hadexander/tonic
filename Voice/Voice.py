import discord
from discord.ext import commands

class Voice:
    @commands.command(pass_context=True)
    async def join(self,ctx):
        if ctx.message.author.voice is None:
            await ctx.bot.send_message(ctx.message.channel, 'You ain\'t there. Can\'t connect')
            return
        await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        await ctx.bot.send_message(ctx.message.channel, "Party times boys!")
        return

    @commands.command(pass_context=True)
    async def disconnect(self,ctx):
        voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        await ctx.bot.send_message(ctx.message.channel, "Crunk time over")
        await voiceclient.disconnect()
        return

    @commands.command(pass_context=True)
    async def playtest(self,ctx):
        voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        if voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not connected to channel, attempting to join")
            #will replace this next section. I know...I know...
            await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
            voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        else:
            await ctx.bot.send_message(ctx.message.channel, "Playing test sound")
        player = voiceclient.create_ffmpeg_player('victory.mp3')
        player.start()
        return
