import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from django.conf import settings
from .handlers import setup


async def bot():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    router = Router()
    
    dp.include_router(router)
    setup(router, bot)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def run():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(bot())