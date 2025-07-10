from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import logging

from config import settings

import app.keyboards as kb
import confirm_esch as cesch
import app.database.requests as rq
from ..parser.main_parser import parser_main

from bot import bot

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.states import Register, Reregister, Admin

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    # await parser_main()
    if await rq.check_user_for_being_in_bd(message.from_user.id) == False:
        await message.answer(
            "Вы уже зарегестрированы! Если хотите сменить логин и пароль, то воспользуйтесь командой /relogin"
        )
    else:
        await message.answer(
            "Привет! Это EschoolBot. Я могу присыласть уведомления о новых оценках.",
            reply_markup=kb.main,
        )


@router.message(Command("parser"))  # just for test
async def parsing(message: Message):
    await parser_main()





# MAIN REGISTRATION
@router.callback_query(F.data == "continue")
async def continue_0(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Регистрация")
    await callback.message.answer(
        "Отлично, для продолжения введите свой логин от Eschool"
    )
    await state.clear()
    await state.set_state(Register.password)


@router.message(Register.password)
async def password(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль")
    await state.set_state(Register.confirm)


@router.message(Register.confirm)
async def confirm(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.update_data(msg_id=message.message_id)
    data = await state.get_data()
    msg = await message.answer(
        f'Данные верны?\nВаш логин: {data["login"]}\nВаш пароль: {data["password"]}',
        reply_markup=kb.reg_keyboard_builder(),
    )
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data == "change")
async def change(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите логин")
    await state.set_state(Register.password)


@router.callback_query(F.data == "continue2")
async def continue_2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    msg_id = data.get("msg_id")
    await bot.delete_message(callback.message.chat.id, msg_id)
    try:
        logging.info("начало проверки regex")
        if await rq.check_passw_with_regex(data, callback.from_user.id):
            logging.info("Удача")
            await callback.message.answer(
                "Вы успешно ввели свой логин и пароль, сейчас попробуем авторизоваться на сайте Eschool, используя ваши данные, это может занять какое-то время"
            )
            if await cesch.small_parser_esch(data, callback.from_user.id):
                await rq.set_password_and_login(data, callback.from_user.id)
                await callback.message.answer(
                    "Авторизация прошла успешно! Вы успешно зарегестрированы!"
                )
                await callback.message.answer(
                    "Когда в вашем электроном жунале появятся новые оценки, бот обязательно пришлет вам об этом уведомление!"
                )
                await state.clear()
            else:
                await callback.message.answer(
                    "Не получилось пройти регестрацию, попробуйте повторно зарегестрироваться"
                )
                await callback.message.answer("Введите свой логин снова")
                await state.set_state(Register.password)
        else:
            logging.info("Неудача")
            await callback.message.answer("Ваши данные некорректны")
            await callback.message.answer("Введите свой логин снова")
            await state.clear()
            await state.set_state(Register.password)
    except Exception as e:
        print(e)
        logging.info("Хрючево")
        await callback.message.answer("Ваши данные некорректны")
        await callback.message.answer("Введите свой логин снова!")
        await state.clear()
        await state.set_state(Reregister.login)


# END OF MAIN REGISTRATION


# RERIGISTRATION!
@router.message(Command("relogin"))
async def re_registraion(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Отлично, для повторной регистрации введите свой логин от Eschool"
    )
    await state.set_state(Reregister.login)


@router.message(Reregister.login)
async def login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль")
    await state.set_state(Reregister.password)


@router.message(Reregister.password)
async def password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    remsg = await message.answer(
        f'Данные верны?\nВаш логин: {data["login"]}\nВаш пароль: {data["password"]}',
        reply_markup=kb.reg_keyboard_builder(True),
    )
    await state.update_data(remsg_id=remsg.message_id)


@router.callback_query(F.data == "relogin_change")
async def change(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите логин")
    await state.set_state(Reregister.login)


@router.callback_query(F.data == "relogin_continue2")
async def continue_2(callback: CallbackQuery, state: FSMContext):
    logging.info("начало проверки regex re")
    await callback.answer()
    data = await state.get_data()
    remsg_id = data.get("remsg_id")
    await bot.delete_message(callback.message.chat.id, remsg_id)
    try:
        if await rq.check_passw_with_regex(data, callback.from_user.id):
            await rq.reset_password_and_login(data, callback.from_user.id)
            await callback.message.answer(
                "Ваш пароль и логин был обновлен, сейчас попробуем авторизоваться на сайте Eschool, используя ваши обновленные данные, это может занять какое-то время"
            )
            if await cesch.small_parser_esch(data, callback.from_user.id):
                await rq.reset_password_and_login(data, callback.from_user.id)
                await callback.message.answer(
                    "Авторизация прошла успешно! Вы успешно повторно зарегестрировались!"
                )
                await callback.message.answer(
                    "Когда в вашем электроном жунале появятся новые оценки, бот обязательно пришлет вам об этом уведомление!"
                )
                await state.clear()
            else:
                await callback.message.answer(
                    "Не получилось пройти регестрацию, попробуйте повторно ещё раз"
                )
                await callback.message.answer("Введите свой логин снова")
                await state.set_state(Reregister.login)

        else:
            await callback.message.answer("Ваши данные некорректны")
            await callback.message.answer("Введите свой логин снова!")
            await state.clear()
            await state.set_state(Reregister.login)
    except TypeError:
        logging.info("Хрючево")
        await callback.message.answer("Ваши данные некорректны")
        await callback.message.answer("Введите свой логин снова!")


@router.message(Reregister.reconfirm_esch)
async def reconfirm_esch(message: Message, state: FSMContext):
    data = await state.get_data()
    if await cesch.small_parser_esch(data, message.from_user.id):
        await rq.reset_password_and_login(data, message.from_user.id)
        await message.answer(
            "Авторизация прошла успешно! Вы успешно повторно зарегестрировались!"
        )
        await state.clear()
    else:
        await message.answer(
            "Не получилось пройти регестрацию, попробуйте повторно ещё раз"
        )
        await message.answer("Введите свой логин снова")
        await state.set_state(Reregister.login)
