from fastapi import FastAPI

from .api_v1 import exception_handlers
from .api_v1.router import router

app = FastAPI(
    exception_handlers={
        exception_handlers.exceptions.ParserException: exception_handlers.parser_exception_handler,
        exception_handlers.exceptions.SchemaException: exception_handlers.schema_exception_handler,
        exception_handlers.exceptions.VerifyException: exception_handlers.verify_exception_handler,
        exception_handlers.RequestValidationError: exception_handlers.request_validation_exception_handler,
    },
    responses={
        200: {},
        422: {
            "content": {
                "application/json": {},
            },
            "description": "Validation Error",
            "model": exception_handlers.ErrorResponse,
        },
    },
)


app.include_router(
    prefix="/v1",
    router=router,
)
