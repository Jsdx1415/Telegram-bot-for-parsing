import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.database.requests as rq
import app.keyboards as kb
import app.parser.confirm_reg as pr
from app.handlers.states_for_registration import Register, Reregister
from bot import bot

router = Router()


# MAIN REGISTRATION
@router.callback_query(F.data == "continue")
async def continue_0(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Регистрация")  # отзываемся на callback
    await callback.message.answer(
        "Отлично, для продолжения введите свой логин от сайта"
    )
    await state.clear()
    await state.set_state(Register.password)


@router.message(Register.password)  # ловим логин
async def password(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль")
    await state.set_state(Register.confirm)


@router.message(Register.confirm)  # ловим пароль и получаем тг айди
async def confirm(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.update_data(msg_id=message.message_id)
    data = await state.get_data()
    msg = await message.answer(
        f'Данные верны?\nВаш логин: {data["login"]}\nВаш пароль: {data["password"]}',  # подтверждаем правильность введенных данных
        reply_markup=kb.reg_keyboard_builder(),
    )
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(
    F.data == "change"
)  # если пользователь передумал, просто проходим все занаво
async def change(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите логин")
    await state.set_state(Register.password)


@router.callback_query(
    F.data == "continue2"
)  # если пользователь подтвердил правильность введных им данных
async def continue_2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    msg_id = data.get("msg_id")
    await bot.delete_message(callback.message.chat.id, msg_id)
    try:
        logging.info("начало проверки regex")
        if await rq.check_passw_with_regex(data, callback.from_user.id):
            logging.info("Данные прошли через regex успешно")
            await callback.message.answer(
                "Вы успешно ввели свой логин и пароль, сейчас попробуем авторизоваться на сайте, используя ваши данные, это может занять какое-то время"
            )
            if await pr.check_parser(
                data, callback.from_user.id
            ):  # вторая волна проверки
                await rq.set_password_and_login(
                    data, callback.from_user.id
                )  # вносим данные в бд
                await callback.message.answer(
                    "Авторизация прошла успешно! Вы успешно зарегестрированы!"
                )
                await callback.message.answer(
                    "Когда появится что-то новое, бот обязательно пришлет вам об этом уведомление!"
                )
                await state.clear()
                logging.info("Новый пользователь был успешно зарегестрирован")
            else:
                await callback.message.answer(
                    "Не получилось пройти регестрацию, попробуйте повторно зарегестрироваться"  # данные пользователя оказались неправильными/неактуальными
                )
                await callback.message.answer("Введите свой логин снова")
                await state.set_state(Register.password)
        else:
            logging.info("Неудача в проверке акуальности данных от сайта")
            await callback.message.answer("Ваши данные некорректны")
            await callback.message.answer("Введите свой логин снова")
            await state.clear()
            await state.set_state(
                Register.password
            )  # отправляем регестрироваться снова
    except Exception as e:
        print(e)
        logging.info("Хрючево")
        await callback.message.answer("Ваши данные некорректны")
        await callback.message.answer("Введите свой логин снова!")
        await state.clear()
        await state.set_state(Reregister.login)  # отправляем регестрироваться снова


# END OF MAIN REGISTRATION
