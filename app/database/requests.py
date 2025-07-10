from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select
from sqlalchemy.sql import and_

import re
import logging

from config import settings
from aiogram.types import Message

from app.crypto.crypto_for_passw import MyCrypto
from regex import pattern


async def check_passw_with_regex(data, tg_id: int):
    async with async_session() as session:
        if re.search(pattern, data["login"]) and re.search(pattern, data["password"]):
            return True
        return False


async def set_password_and_login(data, tg_id: int):
    async with async_session() as session:
        logging.info("Добавление пользователя в таблицу")
        session.add(User(tg_id=tg_id))
        key = settings.key
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.login = data["login"]
        user.password = MyCrypto(key).encrypt(data["password"])
        logging.info("Пользователь был добавлен")
        await session.commit()


async def reset_password_and_login(data, tg_id: int):
    async with async_session() as session:
        logging.info("Передобавление пользователя в таблицу")
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        key = settings.key
        user.login = data["login"]
        user.password = MyCrypto(key).encrypt(data["password"])
        logging.info("Пользователь был повторно добавлен")
        await session.commit()


async def check_user_for_being_in_bd(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user != None and user.tg_id != None:
            return False


async def get_all_users() -> list[dict]:
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.mappings().all()


async def get_all_tg_ids():
    async with async_session() as session:
        res = await session.scalars(select(User.tg_id))
        return res.all()


async def get_all_info_users():
    async with async_session() as session:
        tg_result = await session.scalars(select(User.tg_id))
        tg_ids = tg_result.all()

        # 2) Получаем все login в том же порядке
        login_result = await session.scalars(select(User.login))
        logins = login_result.all()
        return dict(zip(tg_ids, logins))
