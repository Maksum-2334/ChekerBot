import asyncio
from dotenv import load_dotenv
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter

from sqlalchemy.ext.asyncio import AsyncSession

from mails_app.database.requests import change_active


bot = Bot(token=os.getenv('TOKEN'))


def generate_keyboard(
        btn_text: str = None,
        btn_url: str = None,
) -> InlineKeyboardMarkup | None:
    
    btn_builder = InlineKeyboardBuilder()
    btn_builder.row(
        InlineKeyboardButton(
            text=btn_text,
            url=btn_url
        )
    )
    return btn_builder.as_markup()


async def send_preview_with_keyboard(
        message: Message,
        photo: str = None,
        text: str = '',
        btn_text: str = None,
        btn_url: str = None
) -> int:
    keyboard = None

    if btn_text and btn_url:
        keyboard = generate_keyboard(btn_text, btn_url)

    if photo:
        sent_message = await message.answer_photo(caption=text, photo=photo, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        sent_message = await message.answer(text=text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)

    return sent_message.message_id


async def send_preview(
        message: Message,
        data: dict
) -> int:
    
    message_id = await send_preview_with_keyboard(
        message,
        data['msg_photo'],
        data['msg_text'],
        data['btn_text'],
        data['btn_url']
    )

    return message_id


async def send_mail(
        bot: Bot,
        user_id: str,
        from_chat_id: int,
        message_id: int,
        keyboard: InlineKeyboardMarkup = None) -> bool:
    
    try:
        await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id, reply_markup=keyboard)

    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_mail(bot, user_id, from_chat_id, message_id, keyboard)
    
    except Exception as e:
        print(e)
        return False
    else:
        return True


async def start_sender(
        bot: Bot,
        data: dict,
        chats_id,
        from_chat_id: int,
        message_id: int
) -> int:
    
    count = 0
    keyboard = None
    
    if data['btn_text'] and data['btn_url']:
        keyboard = generate_keyboard(data['btn_text'], data['btn_url'])

    for c_id in chats_id:
        if await send_mail(bot, int(c_id), from_chat_id, message_id, keyboard):
            count += 1
        await asyncio.sleep(0.5)

    return count
