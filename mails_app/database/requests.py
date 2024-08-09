from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from mails_app.database.models import Chat
from mails_app.database.models import async_session
from sqlalchemy.exc import NoResultFound


async def get_active_chats():
    async with async_session() as session:
        chats = await session.execute(
            select(Chat.telegram_id)
        )
        all_chats = chats.scalars().all()

        print(all_chats, 'chats all')
        return all_chats


async def get_active_chats_name():
    async with async_session() as session:
        chats_id = await session.execute(
            select(Chat.telegram_id)
        )
        chats_name = await session.execute(
            select(Chat.chat_name)
        )
        
        all_chats_name = chats_name.scalars().all()
        all_chats_id = chats_id.scalars().all()
        
        return [all_chats_name, all_chats_id]


async def add_chat(telegram_id: str, chat_name: str):
    async with async_session() as session:

        query = await session.execute(select(Chat).where(Chat.telegram_id == telegram_id))
        is_exists = query.scalar_one_or_none()
        
        if is_exists:
            return False
        
        chat = Chat(
            telegram_id=telegram_id, 
            chat_name=chat_name
        )
        session.add(chat)
        await session.commit()
        return chat 


async def delete_chat(telegram_id: str):
    async with async_session() as session:
        try:
            result = await session.execute(select(Chat).where(Chat.telegram_id == telegram_id))
            chat = result.scalar_one()

            await session.delete(chat)
            await session.commit()

            return True
        
        except NoResultFound:
            return False
        

async def change_active(session: AsyncSession, telegram_id: str, is_active: bool) -> None:
    await session.execute(update(Chat).filter(Chat.telegram_id == telegram_id).values(is_active=is_active))
    await session.commit()
    