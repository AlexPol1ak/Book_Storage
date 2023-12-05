from typing import Union

from fastapi import FastAPI

from auth.router import auth_router

app = FastAPI(title="Book storage")


@app.get('/')
async def test_page():
    return {"Hello": "World"}
@app.get('/start/{item_id}')
async def start_page_arg(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(auth_router)