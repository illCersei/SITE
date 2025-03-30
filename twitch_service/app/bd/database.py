from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from config import settings

load_dotenv()

DATABASE_URL = settings.DATABASE_URL_ASYNCPG

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """ Асинхронная сессия БД """
    async with AsyncSessionLocal() as session:
        yield session  