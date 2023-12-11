from typing import Union

from fastapi import FastAPI

from user.routers.admin import admin_router
from user.routers.user import user_router

app = FastAPI(title="Book storage")


@app.get('/')
async def test_page():
    return {"Hello": "World"}


@app.get('/start/{item_id}')
async def start_page_arg(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


app.include_router(user_router)
app.include_router(admin_router)
