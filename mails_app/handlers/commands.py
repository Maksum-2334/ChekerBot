from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from mails_app.state.base import CreateMessage


async def create_sender_handler(message: Message, state: FSMContext) -> None:
    await message.answer('*Створення розсилки!*\nЗалиште текст розсилки', parse_mode=ParseMode.MARKDOWN)
    await state.set_state(CreateMessage.get_text)
    