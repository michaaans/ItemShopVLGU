import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.db_requests import orm_create_categories, orm_add_banner_description
from database.models import Base

# инициализируем движок
from src.desc_text import description_for_info_pages, categories

engine = create_async_engine(os.getenv('DB_LITE'), echo=True)

# сессии для запроса к базе данных
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # чтобы категории и превьюшки сразу были созданы при запуске
    async with session_maker() as session:
        await orm_create_categories(session, categories)
        await orm_add_banner_description(session, description_for_info_pages)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
