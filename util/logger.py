import logging
import asyncio

class DiscordLoggingHandler(logging.Handler):
    def __init__(self, bot, channel):
        logging.Handler.__init__(self)
        self.bot = bot
        self.channel = channel
    
    def emit(self, record):
        record_fmt = self.format(record)
        coro = self.bot.send_message(self.channel, record_fmt)
        asyncio.run_coroutine_threadsafe(coro, self.bot.loop)

class DiscordLoggingFormatter(logging.Formatter):
    def format(self, record):
        return "``**{record.levelname}:{record.name}**``\n```{record.msg}```"