import extras
import util
import github
import poe
import Voice
from Voice.Voice import Queue
def setup(bot):
    util.setup(bot)
    poe.setup(bot)
    github.setup(bot)
    extras.setup(bot)
    Voice.setup(bot)
    Queue.setup(bot)
