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
        future = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        try:
            future.result()
        except:
            return

class DiscordLoggingFormatter(logging.Formatter):
    def format(self, record):
        return f"``{record.levelname}:{record.name}``\n```{record.msg}```"

class LoggingErrorWriter:
    def __init__(self, logger):
        self.logger = logger
    
    def write(self, message):
        self.logger.error(message)
