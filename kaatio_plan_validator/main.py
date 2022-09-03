from fastapi import FastAPI

from .api_v1 import routes

app = FastAPI(
    contact={
        "name": "Spatineo Inc.",
        "email": "support@spatineo.com",
    },
    title="Kaava-XML:n simuloitu tallennuspalvelu",
)


app.include_router(
    prefix="/v1",
    router=routes.router,
)
