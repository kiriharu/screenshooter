import typing

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from starlette.exceptions import HTTPException
from pyppeteer.errors import PageError

from screenshooter.schemas import ErrorResponse, Error, ResponseSchema


class AutoJSONResponse(JSONResponse):

    def render(self, content: typing.Any) -> bytes:
        if hasattr(content, "dict"):
            content = content.dict()
        return super().render(content)


async def page_error_handler(request: Request, exc: PageError) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=ResponseSchema(
            data=None,
            error=ErrorResponse(
                msg="Resource name not resolved",
                code=Error.NotResolved
            ),
            success=False
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    exc_resp = ResponseSchema(
        data=None,
        error=ErrorResponse(
            msg=exc.detail,
            code=Error.HTTPException,
        ),
        success=False
    )

    if headers:
        return AutoJSONResponse(
            status_code=exc.status_code, content=exc_resp, headers=headers
        )
    else:
        return AutoJSONResponse(
            content=exc_resp, status_code=exc.status_code
        )
