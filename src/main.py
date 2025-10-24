from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import init_db, async_engine
from .routers.cars import cars_router
from .routers.manufacturers import manufacturer_router
from . import models


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield

    await async_engine.dispose()

app = FastAPI(
    debug=True,
    title='Cars',
    description='Api for car CRUD operations',
    version='0.1.0',
    lifespan=lifespan
)

app.include_router(cars_router)
app.include_router(manufacturer_router)

@app.get('/')
async def read_root():
    return {
        'message': 'Welcome to Api where you can Create, Get, '
                    'Update or Delete information about cars'
    }
