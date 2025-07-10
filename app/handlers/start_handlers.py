import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
import app.database.requests as rq
from ..parser.main_parser import parser_main


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if (
        await rq.check_user_for_being_in_bd(message.from_user.id) == False
    ):  # если кто-то жмет команду старт, будуче уже зарегестрированным
        await message.answer(
            "Вы уже зарегестрированы! Если хотите сменить логин и пароль, то воспользуйтесь командой /relogin"
        )
    else:  # для тех кто в первый раз
        await message.answer(
            "Привет! Это Tg_Bot. Я могу присыласть уведомления о новых оценках.",
            reply_markup=kb.main,
        )


@router.message(Command("parser"))  # just for test
async def parsing(message: Message):
    await parser_main()
