import app.database.requests as rq

import asyncio
import logging
import sys

from playwright.async_api import async_playwright

from config import settings
from .markData import MarkData
from app.crypto import MyCrypto
from config import settings

from aiogram.types import Message

from bot import bot


async def parser_main():
    logging.info("Начало парсинга")
    for user in await rq.get_all_users():
        key = settings.key
        user = user["User"]
        user_passw_ref = MyCrypto(key).decrypt(user.password)
        marks = [
            mark async for mark in parse_data(user.login, user_passw_ref, user.tg_id)
        ]  # берем оценки из parse_data
        # проверка на существование новых оценок
        if not marks:
            pass  # TODO: ну на проде надо это убрать
        else:
            for mark in marks:
                # вывод оценки в виде строки
                await bot.send_message(chat_id=user.tg_id, text=mark.as_str())


async def parse_data(login, password, tg_id):
    logging.info("Продолжение парсинга")
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
            logging.info(msg="Запущен процесс авторизации в системе ESchool.")

            await page.wait_for_selector("#inputLogin", timeout=5000)
            await page.wait_for_selector("#inputPassword", timeout=5000)

            await page.fill("#inputLogin", login)
            await page.fill("#inputPassword", password)  # settings.eschool_password

            await page.wait_for_selector("#btn-login:not([disabled])")
            await page.get_by_role("button", name="Log in").click()  # Log in

            # checking the password for correctness

            await page.wait_for_timeout(100)  # сомнительно, но окэээээй
            locator_passw_err = page.locator(
                ".alert.alert-warning.mb-0.ng-binding",
                has_text="Login/password error",  # Login/password error
            )
            if await locator_passw_err.count() > 0:
                print(
                    "Неверный логин или пароль!"
                )  # ну как бы нужно сменить на норм тему
                await bot.send_message(
                    chat_id=tg_id,
                    text="Неверный логин или пароль! Вам нужно сменить его с помощью команды /relogin",
                )
                return

            await page.wait_for_selector("#today")

            # checking whether the password needs to be changed
            # locator_new_passw = page.locator(".p-0.fancybox-content")

            # if await locator_new_passw.count() > 0:
            #     print(
            #         "Вам нужно сменить пароль!"
            #     )  # ну как бы нужно сменить на норм тему
            #     await bot.send_message(
            #         chat_id=tg_id, text="Вам нужно сменить пароль на сайте ескула!"
            #     )

            await page.wait_for_timeout(700)

            # checking whether user have problems with email
            locator_email_change = page.locator(
                ".main-bg.p-0.overflowVisible.ng-scope.fancybox-content"
            )
            if await locator_email_change.count() > 0:
                await page.get_by_role("button", name="Закрыть").click()

            await page.click("#buttonMenu")

            await page.get_by_text("Оценки за период").nth(1).click()

            await page.wait_for_selector(".p-0.pl-5.text-left.ng-binding", timeout=5000)

            # logging.info(msg="Успешная авторизация.")

            # main parse logic
            logging.info(msg="Инициализация парсинга отметок...")

            elements = page.locator('[id^="cell-mark"]')

            for element in await elements.all():
                await element.is_visible()

                border_style = await element.evaluate(
                    "el => window.getComputedStyle(el).border"
                )
                if not "3px dashed" in border_style:
                    continue

                await page.evaluate(
                    "document.querySelectorAll('#topfake, #topscrl').forEach(el => el.style.display = 'none')"
                )

                await element.click(force=True)

                mark = await element.locator(
                    ".markValInProgress span.ng-binding"
                ).first.inner_text()

                mark_2_locator = element.locator(
                    ".markValInProgress .ng-scope span.ng-binding"
                )

                if await mark_2_locator.count() > 0:
                    mark += "/" + await mark_2_locator.inner_text()

                if not mark.strip():
                    continue

                subject = await page.locator(
                    ".fs-16.p-0.m-0.ng-binding"
                ).first.inner_text()

                theme = await page.locator(
                    ".fw-light.fs-italic.ng-binding"
                ).first.inner_text()

                mark_weight = (
                    await page.locator(".fw-light.fs-italic.ng-binding")
                    .nth(2)
                    .inner_text()
                )

                # возврат объекта в генератор
                yield MarkData(mark, subject, theme, mark_weight)

            logging.info(msg="Парсинг завершен, выход из метода парсинга...")

            await browser.close()

    except Exception as e:
        logging.error(f"Произошла ошибка:\n{e}")
        await browser.close()
        await asyncio.sleep(10)
