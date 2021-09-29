from fastapi import Request
from fastapi.responses import JSONResponse
from pyppeteer.errors import PyppeteerError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def page_error_handler(
    request: Request,
    exc: PyppeteerError,
    details: str = "Resource not resolved"
) -> JSONResponse:
    return JSONResponse(
        dict(details=details),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )
