from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.enums import ParseMode

from mails_app.handlers import sender
from mails_app.keyboard import keyboards as kb
from mails_app.state.base import CreateMessage


router = Router()


@router.message(CreateMessage.get_text, F.text)
async def set_text_handler(message: Message, state: FSMContext):
    await state.update_data(msg_text=message.md_text)

    await message.answer(
        text='Очікування фото',
        reply_markup=kb.get_photo_confirm().as_markup(),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@router.message(CreateMessage.get_photo, F.photo)
async def set_photo_handler(message: Message, state: FSMContext):
    await state.update_data(msg_photo=message.photo[-1].file_id)
    data = await state.get_data()

    await message.answer(
        text='Надішліть текст для кнопки',
        reply_markup=kb.get_inline_confirm().as_markup()
    )


@router.message(CreateMessage.get_keyboard_text, F.text)
async def set_btn_text_handler(message: Message, state: FSMContext):
    await state.update_data(btn_text=message.text)
    await state.set_state(CreateMessage.get_keyboard_url)

    await message.answer(
        text='Надішліть посилання для кнопки'
    )


@router.message(CreateMessage.get_keyboard_url, F.text)
async def set_btn_url_handler(message: Message, state: FSMContext):
    await state.update_data(btn_url=message.text)
    data = await state.get_data()

    message_id = await sender.send_preview(
        message,
        data
    )
    await state.update_data(message_id=message_id)
    
    await message.answer(
        text='*Повідомлення для розсилки сформоване!*\n\nЩоб почати, натисніть кнопку нижче',
        reply_markup=kb.get_kb_confirm().as_markup(),
        parse_mode=ParseMode.MARKDOWN_V2
    )

    await state.set_state(CreateMessage.confirm_sender)
