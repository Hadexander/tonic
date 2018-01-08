from extras.xkcd import Xkcd
from extras.fun import Fun

def setup(bot):
    bot.add_cog(Xkcd())
    bot.add_cog(Fun())
