from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📋 Профиль', callback_data='profile'),
            InlineKeyboardButton(text='✍🏻 Решить тест', callback_data='solve_test'),
        ]
    ]
)
