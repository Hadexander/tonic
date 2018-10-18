import discord
import youtube_dl
from discord.ext import commands
#you're not allowed here! Begone!
class Voice:
    voiceclient=None
    player=None
    volume=0.5
    async def join(self,ctx):
        """Bot joins current user's channel"""
        if ctx.message.author.voice.voice_channel is None:
            await ctx.bot.send_message(ctx.message.channel, 'You ain\'t there. Can\'t connect')
            return False
        elif self.voiceclient is not None:
            if ctx.message.author.voice.voice_channel is not self.voiceclient.channel:
                await self.voiceclient.move_to(ctx.message.author.voice.voice_channel)
                return True
        else:
            await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
            Voice.voiceclient = ctx.bot.voice_client_in(ctx.message.server)
            return True

    async def disconnect(self,ctx):
        """Disconnects from current channel"""
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not even in the channel...? :thinking:")
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, "Crunk time over. Wu-tang out!")
            await Voice.voiceclient.disconnect()
            Voice.voiceclient=None
        return

    def _userinchannel(self,ctx):
        """Checks if user is in channel or same channel as bot. (Take that Nico!)"""
        if ctx.message.author.voice.voice_channel is None:
                return False
        #elif ctx.message.author.voice.voice_channel is not ctx.bot.voice.voice_channel:
        #    return False
        else:
            return True

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
        """Plays youtube links. IE 'https://www.youtube.com/watch?v=mPMC3GYpBHg' """
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "Let me join first.")
            await self.join(ctx)
        if self._userinchannel(ctx):
            try:
                Voice.player = await Voice.voiceclient.create_ytdl_player(url)
            except:
                #raise BadArgument()
                return False
            Voice.player.volume = Voice.volume
            Voice.player.start()
            return True
        return

    async def pause(self,ctx):
        """Pauses current song."""
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "Pause? When I'm not there? ....Really?")
            return
        elif Voice.player is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif not Voice.player.is_playing():
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        else:
            Voice.player.pause()
            await ctx.bot.send_message(ctx.message.channel, "Playback paused.")
            return

    async def resume(self,ctx):
        """Resumes current song."""
        if Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, "Resume? When I'm not there? ....Really?")
            return
        elif Voice.player is None:
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif Voice.player.is_playing():
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing something.")
            return
        else:
            Voice.player.resume()
            await ctx.bot.send_message(ctx.message.channel, "Playback paused.")
            return

    async def stop(self,ctx):
        """Stops current song."""
        if Voice.voiceclient is None:
            return False
        if not Voice.player.is_playing():
            return False
        else:
            Voice.player.stop()
            return True

    def format_volume_bar(self, value):
        """Returns the volume bar string. Expects value = [0.0-2.0]"""
        length = 20
        full = int(value / 2.0 * length)
        bar = "``{}{} {:.0f}%``".format('█' * full, '-' * (length - full), value * 100)
        return bar


    async def setvolume(self,ctx,vol):
        """Sets global volume of stream."""
        if vol > 100 or vol < 0:
            return False
        else:
            Voice.volume = vol/100
            if Voice.player is not None:
                Voice.player.volume = Voice.volume
                return True
            return True
