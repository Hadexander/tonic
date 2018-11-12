from .maintenance import Maintenance
from .info import info

def setup(bot):
    bot.add_command(info)
    bot.add_cog(Maintenance(bot))
    