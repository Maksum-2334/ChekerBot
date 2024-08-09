import asyncio
from mails_app.database.engine import engine, Base
from mails_app.database.models import Chat


# Функція створення бази даних
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Виконання функції створення бази даних
if __name__ == "__main__":
    asyncio.run(create_db())
