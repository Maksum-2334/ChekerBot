from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram import Bot

from sqlalchemy.ext.asyncio import AsyncSession

from mails_app.database import requests as rq
from mails_app.handlers import sender

import time


bot = Bot(token='7163892144:AAHxHW9ArXI1CJCb6370XVfrk7MAEJsy2IU')


async def cancel_sending(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Розсилку було відмінено')
    await state.clear()
    await callback.answer()


async def start_sending(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await callback.message.answer('Розсилка почалась')
    await state.clear()
    await callback.answer()

    chats_id = await rq.get_active_chats()

    t_start = time.time()
    message_id = data.get('message_id')

    count = await sender.start_sender(
        bot=bot,
        data=data,
        chats_id=chats_id,
        from_chat_id=callback.message.chat.id,
        message_id=message_id)
    
    await callback.message.answer(f'Відправлено {count}/{len(chats_id)} за {round(time.time() - t_start)}с')
