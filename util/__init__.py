from util.maintenance import Maintenance
from util.prefix import prefix
from util.randomgeneration import tonictoken
from util.info import info

_no_category = [info, prefix, tonictoken]

def setup(bot):
    for cmd in _no_category:
        bot.add_command(cmd)
    bot.add_cog(Maintenance())
    