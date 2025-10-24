"Main module"
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import init_db, async_engine
from .routers.cars import cars_router
from .routers.manufacturers import manufacturer_router
from . import models  # noqa: F401 pylint: disable=unused-import


@asynccontextmanager
async def lifespan(_app: FastAPI):
    '''Lifespan manager'''
    await init_db()
    yield

    await async_engine.dispose()


app = FastAPI(
    debug=True,
    title='Cars',
    description='REST API for managing cars and manufacturers',
    version='0.1.0',
    lifespan=lifespan
)


app.include_router(cars_router)
app.include_router(manufacturer_router)


@app.get('/')
async def read_root():
    '''Root endpoint with API information.'''
    return {
        'message': 'Welcome to Cars API',
        'version': f'{app.version}',
        'description': f'{app.description}',
        'endpoints': {
            'cars': '/cars',
            'manufacturers': '/manufacturers'
        },
        'documentation': '/docs'
    }
