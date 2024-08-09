from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncio

from dotenv import load_dotenv
import os


load_dotenv()
engine = create_async_engine(os.getenv('SQLITE_PATH'), echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[str] = mapped_column(String(32))
    chat_name: Mapped[str] = mapped_column(String(32), nullable=True)
    


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
