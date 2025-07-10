import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.database.requests as rq
import app.keyboards as kb
import app.parser.confirm_esch as pr
from app.states import Reregister
from bot import bot

router = Router()


# RERIGISTRATION!
@router.message(Command("relogin"))  # начало повторной регистрации
async def re_registraion(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Отлично, для повторной регистрации введите свой логин от сайта"
    )
    await state.set_state(Reregister.login)


@router.message(Reregister.login)
async def login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)  # ловим логин
    await message.answer("Введите пароль")
    await state.set_state(Reregister.password)


@router.message(Reregister.password)
async def password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)  # ловим пароль и получаем тг айди
    data = await state.get_data()
    remsg = await message.answer(
        f'Данные верны?\nВаш логин: {data["login"]}\nВаш пароль: {data["password"]}',
        reply_markup=kb.reg_keyboard_builder(True),
    )
    await state.update_data(remsg_id=remsg.message_id)


@router.callback_query(
    F.data == "relogin_change"
)  # если пользователь передумал, просто проходим все занаво
async def change(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите логин")
    await state.set_state(Reregister.login)


@router.callback_query(
    F.data == "relogin_continue2"
)  # если пользователь подтвердил правильность введных им данных
async def continue_2(callback: CallbackQuery, state: FSMContext):
    logging.info("начало проверки regex")
    await callback.answer()
    data = await state.get_data()
    remsg_id = data.get("remsg_id")
    await bot.delete_message(callback.message.chat.id, remsg_id)
    try:
        if await rq.check_passw_with_regex(data, callback.from_user.id):
            logging.info("Данные прошли через regex успешно")
            await rq.reset_password_and_login(data, callback.from_user.id)
            await callback.message.answer(
                "Ваш пароль и логин был обновлен, сейчас попробуем авторизоваться на сайте, используя ваши обновленные данные, это может занять какое-то время"
            )
            if await pr.check_parser(
                data, callback.from_user.id
            ):  # вторая волна проверки
                await rq.reset_password_and_login(data, callback.from_user.id)
                await callback.message.answer(
                    "Авторизация прошла успешно! Вы успешно повторно зарегестрировались!"
                )
                await callback.message.answer(
                    "Когда появится что-то новое, бот обязательно пришлет вам об этом уведомление!"
                )
                await state.clear()
                logging.info("Новый пользователь был успешно зарегестрирован")
            else:
                await callback.message.answer(
                    "Не получилось пройти регестрацию, попробуйте повторно ещё раз"  # данные пользователя оказались неправильными/неактуальными
                )
                await callback.message.answer("Введите свой логин снова")
                await state.set_state(Reregister.login)

        else:
            logging.info("Неудача в проверке акуальности данных от сайта")
            await callback.message.answer("Ваши данные некорректны")
            await callback.message.answer("Введите свой логин снова!")
            await state.clear()
            await state.set_state(Reregister.login)  # отправляем регестрироваться снова
    except TypeError:
        logging.info("Хрючево")
        await callback.message.answer("Ваши данные некорректны")
        await callback.message.answer("Введите свой логин снова!")


# @router.message(Reregister.reconfirm_esch)
# async def reconfirm_esch(message: Message, state: FSMContext):
#     data = await state.get_data()
#     if await pr.check_parser(data, message.from_user.id):
#         await rq.reset_password_and_login(data, message.from_user.id)
#         await message.answer(
#             "Авторизация прошла успешно! Вы успешно повторно зарегестрировались!"
#         )
#         await state.clear()
#     else:
#         await message.answer(
#             "Не получилось пройти регестрацию, попробуйте повторно ещё раз"
#         )
#         await message.answer("Введите свой логин снова")
#         await state.set_state(Reregister.login)
