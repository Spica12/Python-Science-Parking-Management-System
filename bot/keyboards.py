from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Перегляд машин", callback_data="vehicles")
        ],
        [
            InlineKeyboardButton(text="📲 Паркувальні сповіщення", callback_data="parking_messages")
        ],
        [
            InlineKeyboardButton(text="📒 Звіт про розрахунки", callback_data="report")
        ]
    ]
)

exit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Повернутись назад", callback_data="menu")]
    ]
)