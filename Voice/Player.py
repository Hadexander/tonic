from collections import deque
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from discord.ext import commands
import asyncio

class Player:
    _default_options = {'quiet':False, 'noplaylist':True, 'playlist_items':'1', 'format':'bestaudio/webm[abr>0]/best'}
    _search_options = {'default_search':'ytsearch1', 'quiet':False, 'noplaylist':True, 'playlist_items':'1', 'format':'bestaudio/webm[abr>0]/best'}
    _servers = {}

    def get_server_dict(self, server_id):
        if server_id not in self._servers:
            self._servers[server_id] = {'queue':deque(), 'volume':1.0, 'voice':None, 'player':None}
        return self._servers[server_id]
    
    def in_voice(self, server_id):
        """Returns True if in a voice channel on that server."""
        srv = self.get_server_dict(server_id)
        return srv['voice'] and srv['voice'].channel

    def is_playing(self, server_id):
        """Returns True if playing something on that server."""
        srv = self.get_server_dict(server_id)
        return srv['player'] and srv['player'].is_playing()

    async def _join(self, bot, server_id, voice_channel):
        """Bot joins specific voice channel."""
        if not voice_channel:
            return
        srv = self.get_server_dict(server_id)
        if srv['voice']:
            if voice_channel != srv['voice'].channel:
                await srv['voice'].move_to(voice_channel)
        else:
            srv['voice'] = await bot.join_voice_channel(voice_channel)
    '''
    async def _disconnect(self,ctx):
        """Disconnects from current channel"""
        server_id = ctx.message.server.id
        if server_id not in self.voice_clients:
            await ctx.bot.send_message(ctx.message.channel, "I'm not even in the channel...? :thinking:")
            return
        else:
            await ctx.bot.send_message(ctx.message.channel, "Crunk time over. Wu-tang out!")
            await self.voice_clients[server_id].disconnect()
            del self.voice_clients[server_id]
        return
    '''
    def user_in_channel(self, server_id, user):
        """Checks if both the user and bot are in the same channel."""
        srv = self.get_server_dict(server_id)
        return user.voice.voice_channel and srv['voice'] and user.voice.voice_channel == srv['voice'].channel

    def enqueue(self, server_id, url, title, username):
        """Adds song data to a given server's playback queue."""
        srv = self.get_server_dict(server_id)
        srv['queue'].append( (url, title, username) )

    def dequeue(self, server_id):
        """Returns first data tuple in a given server's queue or None."""
        srv = self.get_server_dict(server_id)
        if len(srv['queue']) <= 0:
            return None
        return srv['queue'].popleft()
    '''
    @commands.command(pass_context=True)
    async def queue(self,ctx):
        """Shows current queued items"""
        await ctx.bot.send_message(ctx.message.channel, "We have about {} songs in queue".format(len(self.QueueURL)) )
        await ctx.bot.send_message(ctx.message.channel, self.QueueURL)
    
    def _autoplay(self,ctx):
        server_id = ctx.message.server.id
        ytdl_opts = {'format': 'bestaudio/webm[abr>0]/best'}
        if self._is_queue_empty():
            asyncio.run_coroutine_threadsafe(self._disconnect(ctx),ctx.bot.loop).result()
            return
        corocall = self.voice_clients[server_id].create_ytdl_player(self.QueueURL[0], ytdl_options=ytdl_opts, after=lambda: self._autoplay(ctx))
        scheduling = asyncio.run_coroutine_threadsafe(corocall,ctx.bot.loop)
        try:
            self.players[server_id] = scheduling.result()
        except Exception as e:
            print(e)
            return #oh no.
        self.players[server_id].start()
        self._removequeue()
        return
    '''
    def _play(self, bot, server_id, url):
        """Starts the ffmpeg player."""
        srv = self.get_server_dict(server_id)
        try:
            srv['player'] = srv['voice'].create_ffmpeg_player(url)
        except:
            #shit's fucked
            return
        srv['player'].volume = srv['volume']
        srv['player'].start()
    
    def _find(self, search_str):
        """Performs a youtube search. Returns ytdl entry or None."""
        ytdl = YoutubeDL(self._search_options)
        try:
            info = ytdl.extract_info(search_str, download=False)
            #functools partial etc?
        except DownloadError:
            #couldn't find results
            return None
        return info

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        """Plays most media urls, such as youtube. If not given a url, attempts a youtube search with given text and plays the first result."""
        server_id = ctx.message.server.id
        requester = ctx.message.author
        #refuse command if we don't know which voice channel to join
        if not self.in_voice(server_id) and not requester.voice.voice_channel:
            await ctx.bot.send_message(ctx.message.channel, "Dude, get in voice first.")
            return
        #warn user that the bot won't jump channels while playing
        if self.in_voice(server_id) and not self.user_in_channel(server_id, requester):
            vcname = self.get_server_dict(server_id)['voice'].channel.name
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing in {}. Get in.".format(vcname))
        #create ytdl instance
        #set quiet: True if needed
        ytdl = YoutubeDL(self._default_options)
        try:
            info = ytdl.extract_info(url, download=False)
        except DownloadError:
            #url was bullshit
            search_kw = ctx.message.content[5:]
            info = self._find(search_kw)
            if not info:
                #no hits
                await ctx.bot.send_message(ctx.message.channel, "No media found.")
        if 'entries' in info:
            #it's a playlist
            #just grab the first item
            info = info['entries'][0]
        #at this point info['url'] should point to our preferred format
        download_url = info['url']
        #get media attributes
        title = info.get('title')
        #add to queue
        self.enqueue(server_id, download_url, title, requester)
        await ctx.bot.send_message(ctx.message.channel, "``+ {}``".format(title))
        #join user's voice channel unless already in voice
        if not self.in_voice(server_id):
            await self._join(ctx.bot, server_id, requester.voice.voice_channel)
        #start playback unless already playing
        if not self.is_playing(server_id):
            self._play(ctx.bot, server_id, download_url)
    '''
    @commands.command(pass_context=True)
    async def next(self,ctx):
        """Skips to the next song in queue."""
        server_id = ctx.message.server.id
        if server_id not in self.voice_clients:
            await ctx.bot.send_message(ctx.message.channel, 'Bruh, I\'m not even in a channel. :thinking:')
            return
        elif self._is_queue_empty():
            await ctx.bot.send_message(ctx.message.channel, 'We ain\'t got no more tunes! Pass the AUX cord!!!!! :pray::skin-tone-4:')
            return
        elif server_id not in self.players:
            await self._play(ctx,self.QueueURL[0])
            self._removequeue()
            return
        elif not self.user_in_channel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try. :information_desk_person::skin-tone-4: ")
            return
        else:
            self.players[server_id].pause()
            await self._play(ctx,self.QueueURL[0])
            self._removequeue()
            await ctx.bot.send_message(ctx.message.channel, 'Here we go skipping again!')
            return

    @commands.command(pass_context=True)
    async def pause(self,ctx):
        """Pauses song"""
        server_id = ctx.message.server.id
        if server_id not in self.voice_clients:
            await ctx.bot.send_message(ctx.message.channel, "Pause? When I'm not there? ....Really?")
            return
        elif server_id not in self.players:
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif not self.players[server_id].is_playing():
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif not self.user_in_channel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try. :information_desk_person::skin-tone-4: ")
            return
        else:
            self.players[server_id].pause()
            await ctx.bot.send_message(ctx.message.channel, "Playback paused.")
            return

    @commands.command(pass_context=True)
    async def resume(self,ctx):
        """Resumes playback"""
        server_id = ctx.message.server.id
        if server_id not in self.voice_clients:
            await ctx.bot.send_message(ctx.message.channel, "Resume? When I'm not there? ....Really?")
            return
        elif server_id not in self.players:
            await ctx.bot.send_message(ctx.message.channel, "I'm not playing anything")
            return
        elif self.players[server_id].is_playing():
            await ctx.bot.send_message(ctx.message.channel, "I'm already playing something.")
            return
        elif not self.user_in_channel(ctx):
            await ctx.bot.send_message(ctx.message.channel, "Nice try. :information_desk_person::skin-tone-4: ")
            return
        else:
            self.players[server_id].resume()
            await ctx.bot.send_message(ctx.message.channel, "Playback paused.")
            return
    '''
    def format_volume_bar(self, value):
        """Returns the volume bar string. Expects value = [0.0-2.0]"""
        length = 20
        full = int(value / 2.0 * length)
        bar = "``{}{} {:.0f}%``".format('█' * full, '-' * (length - full), value * 100)
        return bar

    @commands.command(pass_context=True)
    async def volume(self, ctx, vol=-1):
        """Sets playback volume between 0 and 200."""
        server_id = ctx.message.server.id
        srv = self.get_server_dict(server_id)
        vol = int(vol)
        if self.user_in_channel(server_id, ctx.message.author) and vol <= 200 and vol >= 0:
            srv['volume'] = vol/100
            if srv['player']:
                srv['player'].volume = srv['volume']
        await ctx.bot.send_message(ctx.message.channel, self.format_volume_bar(srv['volume']))
