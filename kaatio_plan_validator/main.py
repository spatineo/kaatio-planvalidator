from fastapi import FastAPI

from .api_v1.router import router as api_v1_router

app = FastAPI()
app.include_router(
    prefix="/v1",
    router=api_v1_router,
)
