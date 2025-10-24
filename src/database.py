'''Database management module'''
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, \
                                    create_async_engine
from sqlmodel import SQLModel
from .settings import settings


async_engine = create_async_engine(
    settings.database_url,
    future=True
)


async def init_db() -> None:
    '''Create all database tables.'''
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    '''FastAPI dependency that yields a database session per request'''
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
