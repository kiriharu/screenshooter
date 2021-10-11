from functools import partial
from urllib.request import Request

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pyppeteer.errors import PageError, BrowserError, NetworkError
from starlette.responses import JSONResponse
from screenshooter.schemas import Error, ErrorType


class ScreenshooterException(Exception):
    pass


class RestrictedAddressException(ScreenshooterException):
    pass


class InvalidTokenException(ScreenshooterException):
    pass


async def exception_handler(
    request: Request, err: Exception, errors: list[Error], status_code: int
) -> JSONResponse:
    return JSONResponse({"detail": jsonable_encoder(errors)}, status_code=status_code)


def add_exception_handlers(app: FastAPI):
    def _exc(errors: list[Error], code: int):
        return partial(exception_handler, errors=errors, status_code=code)

    app.add_exception_handler(
        PageError, _exc([Error(msg="Page error", type=ErrorType.PageError)], 422)
    ),
    app.add_exception_handler(
        BrowserError,
        _exc([Error(msg="Browser error", type=ErrorType.BrowserError)], 422),
    )
    app.add_exception_handler(
        NetworkError,
        _exc(
            [
                Error(
                    msg="Network error or invalid cookies", type=ErrorType.NetworkError
                )
            ],
            400,
        ),
    ),
    app.add_exception_handler(
        ScreenshooterException,
        _exc([Error(msg="Restricted Address", type=ErrorType.RestrictedAddress)], 403),
    )
    app.add_exception_handler(
        InvalidTokenException,
        _exc([Error(msg="Invalid token", type=ErrorType.InvalidToken)], 403),
    )
