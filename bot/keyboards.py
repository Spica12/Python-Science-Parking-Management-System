from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📲 Паркувальні сповіщення", callback_data="parking_messages")
        ],
        [
            InlineKeyboardButton(text="📒 Звіт про розрахунки", callback_data="parking_report")
        ]
    ]
)

iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Повернутись на початок", callback_data="menu")]
    ]
)
