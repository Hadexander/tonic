from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from Voice.Voice import Voice
from discord.ext import commands
class Queue:
    Voice = Voice()
    QueueURL=[]

    @commands.command(pass_context=True)
    async def join(self,ctx):
        """Bot joins current user's channel"""
        if await self.Voice.join(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Party time boys!")
            return True
        else:
            await ctx.bot.send_message(ctx.message.channel, 'This ain\'t it Chief')
            return False

    @commands.command(pass_context=True)
    async def disconnect(self,ctx):
        """Disconnects from current channel"""
        await self.Voice.disconnect(ctx)
        return

    def _userinchannel(self,ctx):
        """Checks if user is in channel or same channel as bot. (Take that Nico!). Hardcheck T/F """
        if ctx.message.author.voice.voice_channel is None:
            return False
        elif ctx.message.author.voice.voice_channel is not self.Voice.voiceclient.channel:
            return False
        else:
            return True

    def _addqueue(self,yturl):
        """Adds url to a queue list in case a song is already playing"""
        self.QueueURL.append(yturl)
        return

    def _removequeue(self):
        """Removes first item in queue list"""
        self.QueueURL.pop(0)
        return
    @commands.command(pass_context=True)
    async def clear(self,ctx):
        """Clears entire queue. Becareful!"""
        self.QueueURL.clear()
        await ctx.bot.send_message(ctx.message.channel, 'Music queue empty. Like this bottle of Gin.')
        return

    def _is_queue_empty(self):
        if len(self.QueueURL) == 0:
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def queue(self,ctx):
        """Shows current queued items"""
        await ctx.bot.send_message(ctx.message.channel, "We have about {} songs in queue".format(len(self.QueueURL)) )
        await ctx.bot.send_message(ctx.message.channel, self.QueueURL)

    @commands.command(pass_context=True)
    async def play(self,ctx,url):
        if not _userinchannel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try")
        """Plays youtube links. IE 'https://www.youtube.com/watch?v=mPMC3GYpBHg' """
        #create ytdl instance
        #set quiet: True if needed
        ytdl_opts = {'quiet': False, 'noplaylist': True, 'playlist_items': '1'}
        ytdl = YoutubeDL(ytdl_opts)
        join_s = True
        validation_play_check = False
        try:
            info = ytdl.extract_info(url, download=False)
        except DownloadError:
            #url was bullshit
            await ctx.bot.send_message(ctx.message.channel, "Unsupported URL")
            return
        if info.get('entries'):
            #it's a playlist
            await ctx.bot.send_message(ctx.message.channel, "Entire playlists are not supported")
            return
        if not self._is_queue_empty():
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing something but I'll add it to the queue!")
            self._addqueue(url)
            return
        if self.Voice.player is None:
            self._addqueue(url)
            validation_play_check = await self.Voice.play(ctx,self.QueueURL[0],self.next(ctx))
            self._removequeue()
            return
        if self.Voice.player.is_playing():
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing something but I'll add it to the queue!")
            self._addqueue(url)
            return
        self._addqueue(url)
        validation_play_check = await self.Voice.play(ctx,self.QueueURL[0],self.next(ctx))
        if not validation_play_check:
            await ctx.bot.send_message(ctx.message.channel, "Playback failed!")
        self._removequeue()
        return


    @commands.command(pass_context=True)
    async def next(self,ctx):
        """Plays song next in queue."""
        if self.Voice.voiceclient is None:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m not even in a channel. :thinking:')
            return
        elif len(self.QueueURL) == 0:
            await ctx.bot.send_message(ctx.message.channel, 'We ain\'t got no more tunes! Pass the AUX cord!!!!! :pray::skin-tone-4:')
            return
        elif self.Voice.player is None:
            await self.Voice.play(ctx,self.QueueURL[0],self.next(ctx))
            self._removequeue()
            return
        else:
            await self.Voice.stop(ctx)
            await self.Voice.play(ctx,self.QueueURL[0],self.next(ctx))
            self._removequeue()
            await ctx.bot.send_message(ctx.message.channel, 'Here we go skipping again!')
            return

    @commands.command(pass_context=True)
    async def pause(self,ctx):
        """Pauses song"""
        await self.Voice.pause(ctx)
        return

    @commands.command(pass_context=True)
    async def stop(self,ctx):
        """Stops playback"""
        if await self.Voice.stop(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Stopping!")
        else:
            await ctx.bot.send_message(ctx.message.channel, "No...")
        return

    @commands.command(pass_context=True)
    async def resume(self,ctx):
        """Resumes playback"""
        await self.Voice.resume(ctx)
        return

    @commands.command(pass_context=True)
    async def setvolume(self,ctx, vol):
        """Sets volume between 0 and 200."""
        vol = int(vol)
        await self.Voice.setvolume(ctx,vol)
        await ctx.bot.send_message(ctx.message.channel, self.Voice.format_volume_bar(vol/100))
        return
