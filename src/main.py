# python 3.11.1

from fastapi import FastAPI

from category.routers.privileged_users import p_category_router
from category.routers.user import category_router
from user.routers.privileged_users import admin_router
from user.routers.user import user_router

app = FastAPI(title="Book storage")


@app.get('/')
async def test_page():
    return {"Hello": "World"}


app.include_router(user_router)
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(p_category_router)
