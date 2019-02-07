import logging
import asyncio
import re
from datetime import datetime

class DiscordLoggingHandler(logging.Handler):
    def __init__(self, bot, channel):
        logging.Handler.__init__(self)
        self.bot = bot
        self.channel = channel
        self.buffer = []
        self.run = True
        asyncio.run_coroutine_threadsafe(self.flush_coro(), self.bot.loop)
    
    def emit(self, record):
        self.buffer.append(self.format(record))
    
    async def flush_coro(self):
        while self.run:
            if len(self.buffer) > 0:
                await self.bot.send_message(self.channel, "\n".join(self.buffer))
                self.buffer.clear()
            await asyncio.sleep(5)
    
    def close(self):
        self.run = False
        self.buffer.clear()
        super.close()

class DiscordLoggingFormatter(logging.Formatter):
    def format(self, r):
        msg = re.sub(r"\u001b\[\d+(?:;\d+)?m", "", r.msg)
        return f"``{r.levelname}:{r.name}@{datetime.now()}\n{msg}``"
