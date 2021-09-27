import typing

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pyppeteer.errors import PyppeteerError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from screenshooter.schemas import ErrorResponse, Error, ResponseSchema


class AutoJSONResponse(JSONResponse):

    def render(self, content: typing.Any) -> bytes:
        if hasattr(content, "dict"):
            content = content.dict()
        return super().render(content)


def error_response(msg: str, code: Error) -> ResponseSchema:
    return ResponseSchema(
        data=None,
        error=ErrorResponse(
            msg=msg,
            code=code
        ),
        success=False
    )


async def page_error_handler(request: Request, exc: PyppeteerError) -> JSONResponse:
    return AutoJSONResponse(
        content=error_response(
            "Resource name not resolved",
            Error.NotResolved
        ),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    return AutoJSONResponse(
        content=error_response(
            "Request validation error",
            Error.UnprocessableEntity
        ),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    exc_resp = error_response(exc.detail, Error.HTTPException)
    if headers:
        return AutoJSONResponse(
            content=exc_resp, status_code=exc.status_code, headers=headers
        )
    else:
        return AutoJSONResponse(
            content=exc_resp, status_code=exc.status_code
        )
