from fastapi import FastAPI


app = FastAPI(
    debug=True,
    title='Cars',
    description='Api for car CRUD operations',
    version='0.1.0'
)

@app.get('/')
async def read_root():
    return {
        'message': 'Welcome to Api where you can Create, Get, '
        'Update or Delete information about cars'
    }
