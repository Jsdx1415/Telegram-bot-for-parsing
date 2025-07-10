from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    login = State()
    password = State()
    confirm = State()


class Reregister(StatesGroup):
    login = State()
    password = State()
    confirm = State()


class Admin(StatesGroup):
    all_message = State()
