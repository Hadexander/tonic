from Voice.Voice import Voice
from Voice.Queue import Queue
def setup(bot):
    bot.add_cog(Voice())
    bot.add_cog(Queue())
