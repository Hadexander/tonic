import discord
from discord.ext import commands

class Voice:

    @commands.command(pass_context=True)
    async def jointest(self,ctx):
        if ctx.message.author.voice is None:
            await ctx.bot.send_message(ctx.message.channel, 'You ain\'t there. Can\'t connect')
            return
        await ctx.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        await ctx.bot.send_message(ctx.message.channel, "Party times boys!")
        return

    @commands.command(pass_context=True)
    async def disconnect(self,ctx):
        await voiceclient = ctx.bot.voice_client_in(ctx.message.guild)        
        await ctx.bot.send_message(ctx.message.channel, "Crunk time over")
        await voiceclient.disconnect()
