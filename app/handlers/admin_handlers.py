import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.database.requests as rq
import app.keyboards as kb
from app.states import Admin
from bot import bot
from config import settings

router = Router()

@router.message(Command("admin"))  # создание админки
async def start_admin(message: Message):
    if message.from_user.id not in settings.admin:
        return await message.answer("У вас недостаточно прав((")
    await message.answer("Вы успешно вошли в админ панель!", reply_markup=kb.admin)
    logging.warning(f"Администратор {message.from_user.id} зашел в админку")


@router.callback_query(F.data == "amount_of_users") # отвечает за "Кол-во пользователей"
async def mesg_for_everyone(callback):
    await callback.answer("Кол-во")
    users = await rq.get_all_tg_ids()
    await callback.message.answer(f"Всего пользователей в базе: {len(users)}")


@router.callback_query(F.data == "msg_for_everyone") # отвечает за "Рассылка"
async def mesg_for_everyone(callback, state: FSMContext):
    await callback.answer("Рассылка")
    await callback.message.answer("Введите ваше сообщение")
    await state.set_state(Admin.all_message)


@router.message(Admin.all_message) # также отвечает за "Рассылка", но тут отправляем сообщение
async def mesg_for_everyone2(message, state):
    users = await rq.get_all_tg_ids()
    mess = message.text
    for i in users:
        await bot.send_message(chat_id=i, text=mess)
    await state.clear()


@router.callback_query(F.data == "list_of_all_users") # отвечает за "Список всех пользователей"
async def mesg_for_everyone(callback):
    await callback.answer("Все пользователи")
    users = await rq.get_all_info_users()
    text = "Список пользователей:\n"
    count = 0
    for i, x in users.items():
        count += 1
        text += str(count) + ")" + str(i) + "---" + str(x) + "\n"
    await callback.message.answer(text)