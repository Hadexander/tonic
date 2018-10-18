import asyncio
import discord
from discord.ext import commands

class Polling:
    @commands.command(pass_context=True)
    async def poll(self, ctx, *args):
        """Starts a voting poll on the channel. Voting is done with reactions. Default duration is 60 seconds."""
        text = '@here ' + ' '.join(args)
        msg = await ctx.bot.send_message(ctx.message.channel, text)
        options = ['👍', '👎']
        for r in options:
            await ctx.bot.add_reaction(msg, r)
        await asyncio.sleep(60)
        msg = await ctx.bot.get_message(ctx.message.channel, msg.id)
        results = {}
        for r in msg.reactions:
            emo = str(r.emoji)
            if emo in options:
                results[emo] = r.count - (1 if r.me else 0)
        m = max(results.values())
        winners = [k for k,v in results.items() if v == m]
        if len(winners) > 1:
            final = 'tie'
        else:
            final = winners[0]
        await ctx.bot.edit_message(msg, "{} [poll closed, result: {}]".format(text, final))
