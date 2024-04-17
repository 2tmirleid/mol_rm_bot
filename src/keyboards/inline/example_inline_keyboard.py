from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def example_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="example", callback_data="example")]
        ],
        resize_keyboard=True
    )