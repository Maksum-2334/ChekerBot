from aiogram import Bot, Dispatcher

import asyncio
import logging
from dotenv import load_dotenv
import os

from mails_app.middleware.database import DataBaseSession
from mails_app.handlers.handler import m_router
from mails_app.database.models import AsyncSessionLocal
from mails_app.handlers.create_mail import router
from mails_app.database.models import async_main


load_dotenv()
dp = Dispatcher()

def set_middleware():
    dp.update.middleware(DataBaseSession(session_pool=AsyncSessionLocal))


async def main():

    bot = Bot(token=os.getenv('TOKEN'))
    dp.include_routers(m_router, router)
    set_middleware()
    await dp.start_polling(bot)


if __name__ == '__main__':

    try:
        asyncio.run(main())
  

    except KeyboardInterrupt:
        print('Program was closed')
        