import logging
import asyncio

from playwright.async_api import async_playwright


async def check_parser(data, tg_id: int):
    logging.info("Начало проверки, заход на сайт")
    login = data["login"]
    password = data["password"]
    try:
        async with async_playwright() as p:
            # browser initialization
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # YOUR CHECK_PARSER LOGIC!!!
            # FUNCTION MUST RETURN TRUE OR FALSE!!

            return True  # только для теста!!!

    except Exception as e:
        logging.error(f"Произошла ошибка:\n{e}")
        await browser.close()
        await asyncio.sleep(10)
