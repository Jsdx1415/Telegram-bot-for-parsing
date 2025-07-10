from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    login = State()
    password = State()
    confirm = State()
    confirm_esch = State()


class Reregister(StatesGroup):
    login = State()
    password = State()
    confirm = State()
    reconfirm_esch = State()


class Admin(StatesGroup):
    all_message = State()
