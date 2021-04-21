from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pyppeteer.errors import PageError

from screenshooter.schemas import ErrorResponse, Error


async def page_error_handler(request: Request, exc: PageError) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=dict(detail=ErrorResponse(
            msg="Resource name not resolved",
            type=Error.NotResolved,
        ).dict()),
    )
