from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def reg_keyboard_builder(relogin: bool = False):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да, все правильно",
                    callback_data="relogin_continue2" if relogin else "continue2",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Нет, хочу ввести данные заново",
                    callback_data="relogin_change" if relogin else "change",
                )
            ],
        ]
    )


main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="continue")]
    ]
)

admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Кол-во пользователей", callback_data="amount")],
        [InlineKeyboardButton(text="Рассылка", callback_data="everyone")],
        [InlineKeyboardButton(text="Список пользователей", callback_data="list")],
    ]
)
