import discord
from discord.ext import commands

class Voice:
    voiceclient=None
    player=None
    @commands.command(pass_context=True)
    async def join(self,ctx):
        if ctx.message.author.voice is None:
            await ctx.bot.send_message(ctx.message.channel, 'You ain\'t there. Can\'t connect')
            return
        await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        Voice.voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        await ctx.bot.send_message(ctx.message.channel, "Party times boys!")
        return

    @commands.command(pass_context=True)
    async def disconnect(self,ctx):
        await ctx.bot.send_message(ctx.message.channel, "Crunk time over")
        await Voice.voiceclient.disconnect()
        Voice.voiceclient=None
        return

    @commands.command(pass_context=True)
    async def playtest(self,ctx):
        voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not connected to channel, attempting to join")
            await self.join(ctx)
        else:
            await ctx.bot.send_message(ctx.message.channel, "Playing test sound")
        Voice.player = voiceclient.create_ffmpeg_player('victory.mp3')
        Voice.player.start()
        return
