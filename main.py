import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.handlers import routers
from app.database.models import async_main
from app.parser.main_parser import parser_main

logging.basicConfig(
    level=logging.INFO,
    filename="py_log.log",
    format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
    filemode="w",  # на проде сменить на a, чтобы не было перезаписи
    force=True,
)
logging.getLogger("aiogram").setLevel(logging.WARNING)


async def main():
    bot = Bot(settings.bot_token)
    await async_main()
    dp = Dispatcher()
    for r in routers:
        dp.include_router(r)

    logging.info("Бот запущен")
    print("Бот включен")
    scheduler.start()
    await dp.start_polling(bot)


scheduler = AsyncIOScheduler()  # Планируем выполнение функции каждые час
scheduler.add_job(
    parser_main, "interval", hours=1
)  # можно сменить на любой требуемый интервал


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот выключен")
        print("Бот выключен")
