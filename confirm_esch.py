import logging
import asyncio

from playwright.async_api import async_playwright


async def small_parser_esch(data, tg_id: int):
    logging.info("Начало проверки, заход в ескул")
    login = data["login"]
    password = data["password"]
    try:
        async with async_playwright() as p:
            # browser initialization
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(
                "https://app.eschool.center/#/Login", wait_until="networkidle"
            )

            # authorization

            await page.wait_for_selector("#inputLogin", timeout=5000)
            await page.wait_for_selector("#inputPassword", timeout=5000)

            await page.fill("#inputLogin", login)
            await page.fill("#inputPassword", password)

            await page.wait_for_selector("#btn-login:not([disabled])")
            await page.get_by_role("button", name="Войти").click()  # Log in

            # checking the password for correctness

            await page.wait_for_timeout(100)  # сомнительно, но окэээээй
            locator_passw_err = page.locator(
                ".alert.alert-warning.mb-0.ng-binding",
                has_text="Ошибка логина/пароля",  # Login/password error
            )
            if await locator_passw_err.count() == 0:
                return True
                logging.info("пароль верный")
            else:
                return False

            await browser.close()

    except Exception as e:
        logging.error(f"Произошла ошибка:\n{e}")
        await browser.close()
        await asyncio.sleep(10)
