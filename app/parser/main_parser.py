import asyncio
import logging

from playwright.async_api import async_playwright

from config import settings
from app.crypto.crypto_for_passw import MyCrypto
from config import settings
import app.database.requests as rq

from bot import bot


async def parser_main():
    logging.info("Начало парсинга")
    for user in await rq.get_all_users():
        key = settings.key
        user = user["User"]
        user_passw_ref = MyCrypto(key).decrypt(user.password)
        info = [
            smth async for smth in parse_data(user.login, user_passw_ref, user.tg_id)
        ]  # берем информацию из parse_data
        # проверка на существование новой информации
        if not info:
            pass
        else:
            for smth in info:
                # вывод информации в виде строки
                await bot.send_message(chat_id=user.tg_id, text=smth.as_str())


async def parse_data(login, password, tg_id):
    logging.info("Продолжение парсинга")
    try:
        async with async_playwright() as p:
            logging.info(msg="Запущен процесс авторизации в системе ESchool.")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            """
            YOUR PARCING LOGIC
            
            """

            logging.info(msg="Парсинг завершен, выход из метода парсинга...")

            await browser.close()

    except Exception as e:
        logging.error(f"Произошла ошибка:\n{e}")
        await browser.close()
        await asyncio.sleep(10)
