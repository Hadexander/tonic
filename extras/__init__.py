from extras.xkcd import Xkcd
from extras.fun import Fun
from extras.emoji import Emoji
from extras.poll import Polling

def setup(bot):
    bot.add_cog(Xkcd())
    bot.add_cog(Fun())
    bot.add_cog(Emoji(bot))
    bot.add_cog(Polling())
