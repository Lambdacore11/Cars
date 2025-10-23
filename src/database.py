import os
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel


async_engine = create_async_engine(
    url=
        (
            f'postgresql+asyncpg://'
            f'{os.environ.get('POSTGRES_USER')}:'
            f'{os.environ.get('POSTGRES_PASSWORD')}@'
            f'{os.environ.get('POSTGRES_HOST')}/'
            f'{os.environ.get('POSTGRES_DB')}'
    ),
    future=True
)

async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session        

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
