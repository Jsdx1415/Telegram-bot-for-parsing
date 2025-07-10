import re
import logging

from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select

from config import settings
from app.crypto.crypto_for_passw import MyCrypto
from app.handlers.regex_for_registration import pattern


async def check_user_for_being_in_bd(
    tg_id: int,
):  # фильтрация уже зарегестрированных пользвателей, при нажатии команды /start
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user != None and user.tg_id != None:
            return False


async def check_passw_with_regex(
    data, tg_id: int
):  # первичная проверка пароля с помощью regex
    async with async_session() as session:
        if re.search(pattern, data["login"]) and re.search(pattern, data["password"]):
            return True
        return False


async def set_password_and_login(data, tg_id: int):  # занесение пользователя в таблицу
    async with async_session() as session:
        logging.info("Добавление пользователя в таблицу")
        session.add(User(tg_id=tg_id))
        key = settings.key
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.login = data["login"]
        user.password = MyCrypto(key).encrypt(data["password"])
        logging.info("Пользователь был добавлен")
        await session.commit()


async def reset_password_and_login(
    data, tg_id: int
):  # перезапись пользователя в таблицу
    async with async_session() as session:
        logging.info("Передобавление пользователя в таблицу")
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        key = settings.key
        user.login = data["login"]
        user.password = MyCrypto(key).encrypt(data["password"])
        logging.info("Пользователь был повторно добавлен")
        await session.commit()


async def get_all_users() -> list[dict]:  # используется в main_parser
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.mappings().all()


async def get_all_tg_ids():  # используется в разделе админки "Рассылка" для получения тг айди всех пользователей и последующей рассылки
    async with async_session() as session:
        res = await session.scalars(select(User.tg_id))
        return res.all()


async def get_all_info_users():  # используется в разделе админки "Список всех пользователей" для получения списка всех пользователей
    async with async_session() as session:
        tg_result = await session.scalars(select(User.tg_id))
        tg_ids = tg_result.all()

        login_result = await session.scalars(select(User.login))
        logins = login_result.all()
        return dict(zip(tg_ids, logins))
