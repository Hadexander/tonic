from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from discord.ext import commands
import asyncio
class Player:
    QueueURL=[]
    voiceclients={}
    players={}
    volumes={}

    async def _join(self,ctx):
        """Bot joins current user's channel"""
        servername = ctx.message.server.name
        voice = None
        if ctx.message.author.voice.voice_channel is None:
            await ctx.bot.send_message(ctx.message.channel, 'You ain\'t there. Can\'t connect')
            return False
        elif servername in self.voiceclients:
            if ctx.message.author.voice.voice_channel is not self.voiceclients[servername].channel:
                await self.voiceclients[servername].move_to(ctx.message.author.voice.voice_channel)
                return True
        else:
            await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
            voice = ctx.bot.voice_client_in(ctx.message.server)
            self.voiceclients[servername] = voice
            self.volumes[servername] = .5
            #Voice.voiceclient = ctx.bot.voice_client_in(ctx.message.server)
            return True


    async def _disconnect(self,ctx):
        """Disconnects from current channel"""
        servername = ctx.message.server.name
        if servername not in self.voiceclients:
            await ctx.bot.send_message(ctx.message.channel, "I'm not even in the channel...? :thinking:")
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, "Crunk time over. Wu-tang out!")
            await self.voiceclients[servername].disconnect()
            del self.voiceclients[servername]
        return

    def _userinchannel(self,ctx):
        """Checks if user is in channel or same channel as bot. (Take that Nico!). Hardcheck T/F """
        servername = ctx.message.server.name
        if ctx.message.author.voice.voice_channel is None:
            return False
        elif ctx.message.author.voice.voice_channel is not self.voiceclients[servername].channel:
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

    def _is_queue_empty(self):
        if len(self.QueueURL) == 0:
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def clear(self,ctx):
        """Clears entire queue. Becareful!"""
        self.QueueURL.clear()
        await ctx.bot.send_message(ctx.message.channel, 'Music queue empty. Like this bottle of Gin.')
        return

    @commands.command(pass_context=True)
    async def join(self,ctx):
        await self._join(ctx)
        return

    @commands.command(pass_context=True)
    async def disconnect(self,ctx):
        await self._disconnect(ctx)
        return

    @commands.command(pass_context=True)
    async def queue(self,ctx):
        """Shows current queued items"""
        await ctx.bot.send_message(ctx.message.channel, "We have about {} songs in queue".format(len(self.QueueURL)) )
        await ctx.bot.send_message(ctx.message.channel, self.QueueURL)

    def _autoplay(self,ctx):
        servername = ctx.message.server.name
        ytdl_opts = {'format': 'bestaudio/webm[abr>0]/best'}
        if self._is_queue_empty():
            return
        corocall = self.voiceclients[servername].create_ytdl_player(self.QueueURL[0], ytdl_options=ytdl_opts, after=lambda: self._autoplay(ctx))
        scheduling = asyncio.run_coroutine_threadsafe(corocall,ctx.bot.loop)
        try:
            self.players[servername] = scheduling.result()
        except Exception as e:
            print(e)
            return #oh no.
        self.players[servername].start()
        self._removequeue()
        return

    async def _play(self,ctx,url):
        """Plays youtube links. IE 'https://www.youtube.com/watch?v=mPMC3GYpBHg' """
        servername = ctx.message.server.name
        if servername not in self.voiceclients:
            await self._join(ctx)
        try:
            ytdl_opts = {'format': 'bestaudio/webm[abr>0]/best'}
            self.players[servername] = await self.voiceclients[servername].create_ytdl_player(url, ytdl_options=ytdl_opts, after=lambda: self._autoplay(ctx))
        except:
                #raise BadArgument()
            return False
        self.players[servername].volume = self.volumes[servername]
        self.players[servername].start()
        return True

    @commands.command(pass_context=True)
    async def play(self,ctx,url):
        """Plays youtube links. IE 'https://www.youtube.com/watch?v=mPMC3GYpBHg' """
        #create ytdl instance
        #set quiet: True if needed
        ytdl_opts = {'quiet': False, 'noplaylist': True, 'playlist_items': '1'}
        ytdl = YoutubeDL(ytdl_opts)
        join_s = True
        validation_play_check = False
        servername = ctx.message.server.name
        try:
            info = ytdl.extract_info(url, download=False)
        except DownloadError:
            #url was bullshit
            await ctx.bot.send_message(ctx.message.channel, "Unsupported URL, I'll try to find a video.")
            search_kw = str(ctx.message.content)
            yt_search = {'quiet': False, 'noplaylist': True, 'playlist_items': '1', 'default_search':search_kw}
            ytdl = YoutubeDL(yt_search)
            info = ytdl.extract_info(url, download=False)
            return info
        if info.get('entries'):
            #it's a playlist
            await ctx.bot.send_message(ctx.message.channel, "Entire playlists are not supported")
            return
        if not self._is_queue_empty():
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing something but I'll add it to the queue!")
            self._addqueue(url)
            return
        if servername not in self.voiceclients:
            self._addqueue(url)
            validation_play_check = await self._play(ctx,self.QueueURL[0])
            self._removequeue()
            return
        if servername in self.players: #This is gross, fix later.
            if self.players[servername].is_playing():
                await ctx.bot.send_message(ctx.message.channel, "I'm already playing something but I'll add it to the queue!")
                self._addqueue(url)
                return
        self._addqueue(url)
        validation_play_check = await self._play(ctx,self.QueueURL[0])
        if not validation_play_check:
            await ctx.bot.send_message(ctx.message.channel, "Playback failed!")
        self._removequeue()
        return


    @commands.command(pass_context=True)
    async def next(self,ctx):
        """Plays song next in queue."""
        servername = ctx.message.server.name
        if servername not in self.voiceclients:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m not even in a channel. :thinking:')
            return
        elif self._is_queue_empty():
            await ctx.bot.send_message(ctx.message.channel, 'We ain\'t got no more tunes! Pass the AUX cord!!!!! :pray::skin-tone-4:')
            return
        elif servername not in self.players:
            await self.voiceclients[servername]._play(ctx,self.QueueURL[0])
            self._removequeue()
            return
        elif not self._userinchannel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try. :information_desk_person::skin-tone-4: ")
            return
        else:
            self.players[servername].stop()
            await self._play(ctx,self.QueueURL[0])
            self._removequeue()
            await ctx.bot.send_message(ctx.message.channel, 'Here we go skipping again!')
            return

    @commands.command(pass_context=True)
    async def pause(self,ctx):
        """Pauses song"""
        servername = ctx.message.server.name
        if servername not in self.voiceclients:
            await ctx.bot.send_message(ctx.message.channel, "Pause? When I'm not there? ....Really?")
            return
        elif servername not in self.players:
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif not self.players[servername].is_playing():
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif not self._userinchannel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try. :information_desk_person::skin-tone-4: ")
            return
        else:
            self.players[servername].pause()
            await ctx.bot.send_message(ctx.message.channel, "Playback paused.")
            return

    @commands.command(pass_context=True)
    async def stop(self,ctx):
        """Stops playback"""
        servername = ctx.message.server.name
        if servername not in self.voiceclients:
            return False
        elif servername not in self.players:
            return False
        if not self.players[servername].is_playing():
            return False
        elif not self._userinchannel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try. :information_desk_person::skin-tone-4: ")
            return
        else:
            self.players[servername].stop()
            return True

    @commands.command(pass_context=True)
    async def resume(self,ctx):
        """Resumes playback"""
        servername = ctx.message.server.name
        if servername not in self.voiceclients:
            await ctx.bot.send_message(ctx.message.channel, "Resume? When I'm not there? ....Really?")
            return
        elif servername not in self.players:
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif self.players[servername].is_playing():
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing something.")
            return
        elif not self._userinchannel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try. :information_desk_person::skin-tone-4: ")
            return
        else:
            self.players[servername].resume()
            await ctx.bot.send_message(ctx.message.channel, "Playback paused.")
            return

    def format_volume_bar(self, value):
        """Returns the volume bar string. Expects value = [0.0-2.0]"""
        length = 20
        full = int(value / 2.0 * length)
        bar = "``{}{} {:.0f}%``".format('█' * full, '-' * (length - full), value * 100)
        return bar

    @commands.command(pass_context=True)
    async def setvolume(self,ctx, vol):
        """Sets volume between 0 and 200."""
        servername = ctx.message.server.name
        vol = int(vol)
        if vol > 200 or vol < 0:
            return False
        else:
            self.volumes[servername] = vol/100
            await ctx.bot.send_message(ctx.message.channel, self.format_volume_bar(self.volumes[servername]))
            if servername in self.players:
                self.players[servername].volume = self.volumes[servername]
                return True
            return True
        return
