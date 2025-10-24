"Main module"
from fastapi import FastAPI
from .routers.cars import cars_router
from .routers.manufacturers import manufacturer_router


app = FastAPI(
    debug=True,
    title='Cars',
    description='REST API for managing cars and manufacturers',
    version='0.1.0',
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
