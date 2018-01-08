from discord.ext import commands
from extras.imgur import image_upload

class Emoji:
    @commands.command(pass_context=True)
    async def emo(self, ctx, url):
        """Test imgur upload."""
        link = await image_upload(url)
        await ctx.bot.send_message(ctx.message.channel, link)
