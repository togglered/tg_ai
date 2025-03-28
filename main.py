import asyncio
import logging
import sys

import tg_bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(tg_bot.start())
