from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = InlineKeyboardMarkup(  # самая первая клавиатура для декоративной кнопки "продолжить"
    inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="continue")]
    ]
)


def reg_keyboard(
    relogin: bool = False,
):  # клавиатура для потдверждения введенных пользователем данных при регистрации
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


admin = InlineKeyboardMarkup(  # клавиатура для админки
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Кол-во пользователей", callback_data="amount_of_users"
            )
        ],
        [InlineKeyboardButton(text="Рассылка", callback_data="msg_for_everyone")],
        [
            InlineKeyboardButton(
                text="Список пользователей", callback_data="list_of_all_users"
            )
        ],
    ]
)
