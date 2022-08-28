import uvicorn
from api_v1.router import router as api_v1_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(
    prefix="/v1",
    router=api_v1_router,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
