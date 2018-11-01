import asyncio
import functools
import datetime
from collections import deque
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from discord.ext import commands
from discord import Game

class Player:
    _default_options = {'quiet':False, 'noplaylist':True, 'playlist_items':'1', 'format':'bestaudio/webm[abr>0]/best'}
    _search_options = {'default_search':'ytsearch1', 'quiet':False, 'noplaylist':True, 'playlist_items':'1', 'format':'bestaudio/webm[abr>0]/best'}
    _servers = {}

    def get_server_dict(self, server_id):
        if server_id not in self._servers:
            self._servers[server_id] = {'queue':deque(), 'volume':1.0, 'voice':None, 'player':None, 'song':None}
        return self._servers[server_id]
    
    def in_voice(self, server_id):
        """Returns True if in a voice channel on that server."""
        srv = self.get_server_dict(server_id)
        return srv['voice'] and srv['voice'].channel

    def is_playing(self, server_id):
        """Returns True if in voice and playing something on that server."""
        srv = self.get_server_dict(server_id)
        return srv['voice'] and srv['voice'].channel and srv['player'] and srv['player'].is_playing()

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

    async def _leave(self, server_id):
        """Leaves voice on a specific server."""
        srv = self.get_server_dict(server_id)
        if srv['voice'] and srv['voice'].channel:
            await srv['voice'].disconnect()
            srv['voice'] = None

    def user_in_channel(self, server_id, user):
        """Checks if both the user and bot are in the same channel."""
        srv = self.get_server_dict(server_id)
        return user.voice.voice_channel and srv['voice'] and user.voice.voice_channel == srv['voice'].channel

    def enqueue(self, server_id, url, title, duration, user):
        """Adds song data to a given server's playback queue."""
        srv = self.get_server_dict(server_id)
        srv['queue'].append( (url, title, duration, user) )

    def dequeue(self, server_id):
        """Returns first data tuple in a given server's queue or None."""
        srv = self.get_server_dict(server_id)
        if len(srv['queue']) <= 0:
            return None
        return srv['queue'].popleft()

    def get_nick(self, user):
        nick = user.nick
        if not nick:
            nick = user.name
        return nick
    
    def format_song_display(self, prefix, title, duration, user):
        return "``{} {} [{}] [{}]``\n".format(prefix, title, duration, user)
    
    @commands.command(pass_context=True)
    async def queue(self, ctx):
        """Shows currently queued items."""
        srv = self.get_server_dict(ctx.message.server.id)
        que = srv['queue']
        msg = self.format_song_display('▶', srv['song'][1], srv['song'][2], srv['song'][3])
        i = 1
        for item in que:
            line = self.format_song_display(i, item[1], item[2], item[3])
            i += 1
            msg += line
        await ctx.bot.send_message(ctx.message.channel, msg)
    
    def _after(self, bot, server_id):
        coro = self._play(bot, server_id)
        future = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        try:
            future.result()
        except:
            #shit's more fucked
            return

    async def _finish_playback(self, bot, server_id):
        await self._leave(server_id)
        await bot.change_presence(game = None)
        srv = self.get_server_dict(server_id)
        srv['player'] = None
    
    async def _play(self, bot, server_id):
        """Starts the ffmpeg player with the next song in queue."""
        srv = self.get_server_dict(server_id)
        srv['song'] = self.dequeue(server_id)
        if not srv['song']:
            await self._finish_playback(bot, server_id)
            return
        try:
            srv['player'] = srv['voice'].create_ffmpeg_player(srv['song'][0], after=lambda: self._after(bot, server_id))
            await bot.change_presence(game = Game(name=srv['song'][1]))
        except:
            #shit's fucked
            #not sure what to do in this case?
            await self._finish_playback(bot, server_id)
            return
        srv['player'].volume = srv['volume']
        srv['player'].start()
    
    async def _find(self, bot, search_str):
        """Performs a youtube search. Returns ytdl entry or None."""
        ytdl = YoutubeDL(self._search_options)
        try:
            func = functools.partial(ytdl.extract_info, search_str, download=False)
            info = await bot.loop.run_in_executor(None, func)
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
        await ctx.bot.send_typing(ctx.message.channel)
        ytdl = YoutubeDL(self._default_options)
        try:
            info = ytdl.extract_info(url, download=False)
        except DownloadError:
            #url was bullshit
            search_kw = ctx.message.content[5:]
            info = await self._find(ctx.bot, search_kw)
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
        duration = ''
        if info.get('is_live'):
            duration = 'LIVE'
        else:
            seconds = info.get('duration')
            if seconds:
                duration = str(datetime.timedelta(seconds=seconds))
        nick = self.get_nick(requester)
        #add to queue
        self.enqueue(server_id, download_url, title, duration, nick)
        await ctx.bot.send_message(ctx.message.channel, self.format_song_display('+', title, duration, nick))
        #join user's voice channel unless already in voice
        if not self.in_voice(server_id):
            await self._join(ctx.bot, server_id, requester.voice.voice_channel)
        #start playback unless already playing
        if not self.is_playing(server_id):
            await self._play(ctx.bot, server_id)

    @commands.command(pass_context=True)
    async def next(self, ctx):
        """Skips to the next song in queue."""
        server_id = ctx.message.server.id
        srv = self.get_server_dict(server_id)
        requester = ctx.message.author
        #silentrly drop if not in voice
        if not self.in_voice(server_id):
            return
        #refuse if user not in the same channel
        if not self.user_in_channel(server_id, requester):
            vcname = self.get_server_dict(server_id)['voice'].channel.name
            await ctx.bot.send_message(ctx.message.channel, "You can't control me outside of {}.".format(vcname))
            return
        if self.is_playing(server_id):
            srv['player'].stop()
        else:
            await self._play(ctx.bot, server_id)

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        """Pauses or resumes playback."""
        server_id = ctx.message.server.id
        srv = self.get_server_dict(server_id)
        requester = ctx.message.author
        #silentrly drop if not in voice
        if not self.in_voice(server_id):
            return
        #refuse if user not in the same channel
        if not self.user_in_channel(server_id, requester):
            vcname = self.get_server_dict(server_id)['voice'].channel.name
            await ctx.bot.send_message(ctx.message.channel, "You can't control me outside of {}.".format(vcname))
            return
        if self.is_playing(server_id):
            srv['player'].pause()
        else:
            srv['player'].resume()

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
