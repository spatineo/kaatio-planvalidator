from fastapi import FastAPI

from .api_v1 import routes

app = FastAPI()


app.include_router(
    prefix="/v1",
    router=routes.router,
)
