
from fastapi import FastAPI

from user.routers.privileged_users import admin_router
from user.routers.user import user_router

app = FastAPI(title="Book storage")


@app.get('/')
async def test_page():
    return {"Hello": "World"}


app.include_router(user_router)
app.include_router(admin_router)
