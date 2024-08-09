from aiogram.fsm.state import StatesGroup, State


class CreateMessage(StatesGroup):
    get_text = State()
    get_photo = State()
    get_keyboard_text = State()
    get_keyboard_url = State()
    sending_time = State()
    confirm_sender = State()
    

class AddChatState(StatesGroup):
    waiting_for_chat_name = State()
    waiting_for_chat_id = State()


class DeletedChat(StatesGroup):
    waiting_for_chat_id = State()
    

class SendTime(StatesGroup):
    sending_time = State()
