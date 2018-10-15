import discord
import youtube_dl
from discord.ext import commands
#you're not allowed here! Begone!
class Voice:
    voiceclient=None
    player=None
    volume=0.5
    async def join(self,ctx):
        if ctx.message.author.voice is None:
            await ctx.bot.send_message(ctx.message.channel, 'You ain\'t there. Can\'t connect')
            return
        await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        Voice.voiceclient = ctx.bot.voice_client_in(ctx.message.server)
        await ctx.bot.send_message(ctx.message.channel, "Party times boys!")
        return

    async def disconnect(self,ctx):
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not even in the channel...? :thinking:")
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, "Crunk time over")
            await Voice.voiceclient.disconnect()
            Voice.voiceclient=None
        return

    @commands.command(pass_context=True)
    async def playtest(self,ctx):
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not connected to channel, attempting to join")
            await self.join(ctx)
            Voice.player = Voice.voiceclient.create_ffmpeg_player('victory.mp3')
            Voice.player.start()
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, "Playing test sound")
        if Voice.player is None:
            Voice.player = Voice.voiceclient.create_ffmpeg_player('victory.mp3')
            Voice.player.start()
            return
        else:
            #something truly went wrong if we reach here
            return
        return

    async def play(self,ctx,url):
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "Let me join first.")
            await self.join(ctx)
        Voice.player = await Voice.voiceclient.create_ytdl_player(url)
        Voice.player.volume = Voice.volume
        Voice.player.start()
        return

    async def pause(self,ctx):
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "Pause? When I'm not there? ....Really?")
            return
        if Voice.player is None or not Voice.player.is_playing():
            return
            await ctx.bot.send_message(ctx.message.channel, "Not even playing anything :sus:")
        else:
            await Voice.player.pause()
            await ctx.bot.send_message(ctx.message.channel, "Playback paused.")
            return

    async def stop(self,ctx):
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "Can't stop things if I'm not there")
            return
        if Voice.player is None or not Voice.player.is_playing():
            await ctx.bot.send_message(ctx.message.channel, "Not even playing anything :sus:")
            return
        else:
            await Voice.player.stop()
            await ctx.bot.send_message(ctx.message.channel, "Stopping!")
            return

    async def setvolume(self,ctx,vol):
        if vol < 200 or vol < 0:
            await ctx.bot.send_message(ctx.message.channel, "Please set volume higher than 0 and lower than 200")
            return
        else:
            Voice.volume = vol/100
            await ctx.bot.send_message(ctx.message.channel, "Volume is set to" + Voice.volume)
