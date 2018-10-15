import discord
import youtube_dl
from discord.ext import commands

class Voice:
    voiceclient=None
    player=None
    #@commands.command(pass_context=True)
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
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not connected to channel, attempting to join")
            #will fix later.
            #await self.join(ctx)
            await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
            Voice.voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        else:
            await ctx.bot.send_message(ctx.message.channel, "Playing test sound")
        if Voice.player is None:
            Voice.player = voiceclient.create_ffmpeg_player('victory.mp3')
            Voice.player.start()
        elif Voice.player.is_playing():
            #Need to create queue functionality for this
            return
        else:
            #something truly went wrong if we reach here
            return
        return

    @commands.command(pass_context=True)
    async def play(self,ctx,url):
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "Let me join first.")
        elif Voice.player is not None and Voice.player.is_live():
            #queue system needed
        else:
            Voice.player = await Voice.voiceclient.create_ytdl_player(url)
            Voice.player.start()
