import discord
from discord.ext import commands
from extras.imgur import image_upload, image_delete
from storage.lookups import find_emoji

def _emoji_embed(emoji):
    embed = discord.Embed()
    embed.set_image(url = emoji.url)
    embed.set_footer(text = emoji.name)
    return embed

class Emoji:
    @commands.command(pass_context=True)
    async def emsave(self, ctx, url, name):
        """Saves an emoji to my gallery."""
        data = await image_upload(url)
        if('error' in data):
            await ctx.bot.send_message(ctx.message.channel, 'Upload failed. '+data['error'])
            return
        e = find_emoji(name)
        e.url = data['link']
        e.name = name
        e.id = data['id']
        e.save()
        await ctx.bot.send_message(ctx.message.channel, 'Saved '+name)
    
    @commands.command(pass_context=True)
    async def em(self, ctx, name):
        """Repost an emoji from my gallery."""
        e = find_emoji(name)
        if(e.url):
            await ctx.bot.send_message(ctx.message.channel, embed = _emoji_embed(e))

    @commands.command(pass_context=True)
    async def emdelete(self, ctx, name):
        """Removes an emoji from my gallery."""
        e = find_emoji(name)
        if(e.id):
            await image_delete(e.id)
            e.remove()
            await ctx.bot.send_message(ctx.message.channel, 'Deleted '+name)
