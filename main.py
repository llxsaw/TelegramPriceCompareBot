import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import price_check
from handlers.start import router as start_router
from handlers.price_check import router as price_router
from handlers.notifications import router as notification_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(price_router)
    dp.include_router(notification_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())