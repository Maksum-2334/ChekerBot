from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Почати розсилку')],
    [KeyboardButton(text='Налаштування чатів')]
], resize_keyboard=True)

def change_chats() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Додати чат', callback_data='adding_chat'),
        InlineKeyboardButton(text='Видалити чат', callback_data='deleted_chat')
    )
    return builder


def get_kb_confirm() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Відправити заре', callback_data='start'),
        InlineKeyboardButton(text='Відміна', callback_data='cancel')
    )
    return builder


def get_photo_confirm() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Повідомлення з фото', callback_data='message_with_photo'),
        InlineKeyboardButton(text='Повідомлення без фото', callback_data='message_without_photo')
    )
    return builder


def get_inline_confirm() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Повідомлення з кнопкою з посиланням', callback_data='message_with_inline'),
        InlineKeyboardButton(text='Повідомлення без кнопки з посиланням', callback_data='message_without_inline')
    )
    return builder
