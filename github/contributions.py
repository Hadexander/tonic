import aiohttp
import cairosvg
import PIL
import discord
from discord.ext import commands
from io import BytesIO
from storage.lookups import find_user

@commands.command(pass_context=True)
async def mygit(ctx):
    user = find_user(ctx.message.author.id)
    if not user.github:
        await ctx.bot.send_message(ctx.message.channel, 'You need to register your github profile first.')
        return
    name = user.github
    url = 'https://github.com/users/{}/contributions'.format(name)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if(response.status != 200):
                return
            image = cairosvg.svg2png(bytestring=await response.read(), dpi=70)
    with BytesIO(image) as f:
        with PIL.Image.open(f) as fg:
            with PIL.Image.new(mode = fg.mode, size = fg.size, color='#ffffff') as bg:
                with PIL.Image.alpha_composite(bg, fg) as final:
                    with BytesIO() as output:
                        final.save(output, 'PNG')
                        output.seek(0)
                        msg = await ctx.bot.send_file(ctx.message.channel, fp=output, filename='contributions.png')
    await embed_mygit(ctx, msg, name)

async def embed_mygit(ctx, message, name):
    title = '{} ({})'.format(ctx.message.author.name, name)
    giturl = 'https://github.com/{}'.format(name)
    image = message.attachments[0]
    embed = discord.Embed(title=title, url=giturl, colour=discord.Colour.green(), timestamp=message.timestamp)
    embed.set_image(url=image['url'])
    await ctx.bot.send_message(ctx.message.channel, embed=embed)
    await ctx.bot.delete_message(message)