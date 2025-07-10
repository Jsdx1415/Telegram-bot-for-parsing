import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import logging

from app.handlers.handlers import router as registration_router
from app.handlers.admin_handlers import router as admin_router
from app.database.models import async_main
from app.parser.main_parser import parser_main

logging.basicConfig(
    level=logging.INFO,
    filename="py_log.log",
    format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
    filemode="w",
    force=True,
)
logging.getLogger("aiogram").setLevel(logging.WARNING)
# на проде сменить на a


async def main():
    from bot import bot

    await async_main()
    dp = Dispatcher()
    dp.include_router(registration_router)
    dp.include_router(admin_router)

    logging.info("Бот запущен")
    print("Бот включен")
    scheduler.start()
    await dp.start_polling(bot)


scheduler = AsyncIOScheduler()  # Планируем выполнение функции каждые час
scheduler.add_job(
    parser_main, "interval", hours=1
)  # дада, надо потом будет сменить hours = 1 (minutes=3)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот выключен")
        print("Бот выключен")
