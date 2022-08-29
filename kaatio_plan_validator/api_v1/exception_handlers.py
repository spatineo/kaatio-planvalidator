from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import exceptions


class Error(BaseModel):
    message: str
    reason: list[str]


class ErrorResponse(BaseModel):
    detail: list[Error]


def parser_exception_handler(request: Request, exc: exceptions.ParserException):
    error_res = ErrorResponse(
        detail=[
            Error(
                message=exc.message,
                reason=[exc.reason],
            )
        ]
    )
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def schema_exception_handler(request: Request, exc: exceptions.SchemaException):
    error_res = ErrorResponse(
        detail=[
            Error(
                message=exc.message,
                reason=[exc.reason],
            )
        ]
    )
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def validate_exception_handler(request: Request, exc: exceptions.ValidateException):
    error_res = ErrorResponse(
        detail=[
            Error(
                message=exc.message,
                reason=[],
            )
        ]
    )
    print("ERRR", error_res)
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {
        "detail": [
            {
                "message": err["msg"],
                "reason": [err["type"]],
            }
        ]
        for err in exc.errors()
    }
    error_res = ErrorResponse(**errors)
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
