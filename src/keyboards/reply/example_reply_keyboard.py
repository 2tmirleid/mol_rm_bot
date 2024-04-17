from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def example_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='example')]
        ],
        resize_keyboard=True
    )