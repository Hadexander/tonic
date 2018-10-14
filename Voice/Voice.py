import discord
from discord.ext import commands

class Voice:

    @commands.command(pass_context=True)
    async def _jointest_(ctx):
        if ctx.message.author.voice is None:
            ctx.bot.send_message(ctx.message.channel, 'You ain\'t there. Can\'t connect')
            return
        client.join_voice_channel(ctx.message.author.voice.channel)
        ctx.bot.send_message(ctx.message.channel, "Party times boys!")
        return

    @commands.command(pass_context=True)
    async def _disconnect_():
        Disconnect()
