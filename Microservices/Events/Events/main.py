from fastapi import FastAPI
from fastapi.param_functions import Depends
from tortoise.contrib.fastapi import register_tortoise
from events_app import events
from dependencies import UserOutPydantic, get_current_user_util


app = FastAPI()
app.include_router(events.router)

register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={
        'models': ['models'],
    },
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/")
async def testing():
    return {
        "message": "OK",
    }

@app.get('/api/users/me', response_model=UserOutPydantic)
async def get_current_user(user: UserOutPydantic=Depends(get_current_user_util)):
    return user