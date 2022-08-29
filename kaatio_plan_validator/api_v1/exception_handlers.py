from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import exceptions


class Error(BaseModel):
    message: str
    reason: list[str]
    type: str


class ErrorResponse(BaseModel):
    detail: list[Error]


def parser_exception_handler(request: Request, exc: exceptions.ParserException):
    error_res = ErrorResponse(
        detail=[
            Error(
                message=exc.message,
                reason=[exc.reason],
                type=exc.type,
            )
        ]
    )
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        type=exc.type,
    )


async def schema_exception_handler(request: Request, exc: exceptions.SchemaException):
    error_res = ErrorResponse(
        detail=[
            Error(
                message=exc.message,
                reason=[exc.reason],
                type=exc.type,
            )
        ]
    )
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def verify_exception_handler(request: Request, exc: exceptions.VerifyException):
    error_res = ErrorResponse(
        detail=[
            Error(
                message=exc.message,
                reason=[exc.reason],
                type=exc.type,
            )
        ]
    )
    return JSONResponse(
        content=jsonable_encoder(error_res.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = ErrorResponse(
        detail=[
            {
                "message": err["msg"],
                "reason": [str(err)],
                "type": err["type"],
            }
            for err in exc.errors()
        ]
    )
    return JSONResponse(
        content=jsonable_encoder(errors.detail[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
