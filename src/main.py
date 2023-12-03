from typing import Union

from fastapi import FastAPI

app = FastAPI(title="Trading App")

@app.get('/')
async def test_page():
    return {"Hello": "World"}
@app.get('/start/{item_id}')
async def start_page_arg(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}