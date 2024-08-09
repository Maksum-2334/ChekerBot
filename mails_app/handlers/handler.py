from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from mails_app.handlers.commands import create_sender_handler
from mails_app.handlers import callback as clb
from mails_app.state.base import CreateMessage, AddChatState, DeletedChat
from mails_app.handlers import sender
from mails_app.keyboard import keyboards as kb
from mails_app.database import requests as rq

from sqlalchemy.ext.asyncio import AsyncSession


m_router = Router()


@m_router.message(CommandStart())
async def start(message: Message):
    await message.answer('Вас вітає бот розсилки оберіть дію ', reply_markup=kb.main_kb)


@m_router.message(F.text == 'Почати розсилку')
async def create_sender(message: Message, state: FSMContext):
    await create_sender_handler(message, state)


@m_router.message(F.text == 'Налаштування чатів')
async def chats_settings(message: Message):
    all_chats = await rq.get_active_chats_name()
    text = ''
    for name, chat_id in zip(all_chats[0], all_chats[1]):
        text += f'{name} : {chat_id}\n' 
    print(text)

    if text:
        await message.answer(text=str(text), reply_markup=kb.change_chats().as_markup())
    else:
        await message.answer(text='Чатів немає, спочатку додайте їх: ', reply_markup=kb.change_chats().as_markup())


@m_router.callback_query(F.data == 'adding_chat')
async def adding_chat(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введіть ім`я чату: ')
    await state.set_state(AddChatState.waiting_for_chat_name)

    await callback.answer()


@m_router.message(AddChatState.waiting_for_chat_name)
async def process_chat_name(message: Message, state: FSMContext):
    chat_name = message.text

    await state.update_data(chat_name=chat_name)

    await message.answer('Тепер введіть ID чату:')
    await state.set_state(AddChatState.waiting_for_chat_id)


@m_router.message(AddChatState.waiting_for_chat_id)
async def process_chat_id(message: Message, state: FSMContext):
    chat_id = int(message.text)
    
    #if not chat_id.isdigit():
       # await message.answer('Введіть числовий ID чату')

    chat_id = int(chat_id)

    data = await state.get_data()
    chat_name = data['chat_name']
    
    # Зберігаємо новий чат у базу даних
    await rq.add_chat(chat_name=chat_name, telegram_id=chat_id)
    
    await message.answer(f"Чат '{chat_name}' з ID {chat_id} успішно додано.")
    
    # Скидаємо стан
    await state.clear()


@m_router.callback_query(F.data == 'deleted_chat')
async def deleted_chat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.answer('Введіть ID чату для видалення:')
    await state.set_state(DeletedChat.waiting_for_chat_id)


@m_router.message(DeletedChat.waiting_for_chat_id)
async def process_delete_chat(message: Message, state: FSMContext):
    chat_id = message.text

    data = await state.get_data()
    res = await rq.delete_chat(chat_id)
    if res:

        await message.answer(f'Чат {chat_id} було видалено.')
    else:

        await message.answer(f'Чат {chat_id} не знайдено')

    await state.clear()


@m_router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await clb.cancel_sending(callback, state)


@m_router.callback_query(F.data == 'start')
async def start(callback: CallbackQuery, state: FSMContext):
    await clb.start_sending(callback, state)


@m_router.callback_query(F.data == 'message_with_photo')
async def with_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Очікування фото...')
    await state.set_state(CreateMessage.get_photo)


@m_router.callback_query(F.data == 'message_without_photo')
async def without_photo(callback: CallbackQuery, state: FSMContext):
    await state.update_data(msg_photo=False)
    data = await state.get_data()
    
    await state.set_state(CreateMessage.get_keyboard_text)

    await callback.answer()
    await callback.message.answer(
        text='Оберіть чи потрібен вам посилання знизу: ',
        reply_markup=kb.get_inline_confirm().as_markup()
    )



@m_router.callback_query(F.data == 'message_with_inline')
async def with_inline(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Надішліть текст для кнопки: ')
    await state.set_state(CreateMessage.get_keyboard_text)


@m_router.callback_query(F.data == 'message_without_inline')
async def without_inline(callback: CallbackQuery, state: FSMContext):
    await state.update_data(btn_text=None, btn_url=None)
    data = await state.get_data()
    await callback.answer()

    message_id = await sender.send_preview(
        callback.message,
        data
    )
    await state.update_data(message_id=message_id)
    
    await callback.message.answer(
        text='*Повідомлення для розсилки сформоване!*\n\nЩоб почати, натисніть кнопку нижче',
        reply_markup=kb.get_kb_confirm().as_markup(),
        parse_mode=ParseMode.MARKDOWN
    )

    await state.set_state(CreateMessage.confirm_sender)
