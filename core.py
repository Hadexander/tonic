import extras
import util
import github
import poe

def setup(bot):
    util.setup(bot)
    poe.setup(bot)
    github.setup(bot)
    extras.setup(bot)
