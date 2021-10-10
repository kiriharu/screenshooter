from urllib.request import Request

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from screenshooter.schemas import Error


async def exception_handler(
    request: Request, err: Exception, errors: list[Error], status_code: int
) -> JSONResponse:
    return JSONResponse({"detail": jsonable_encoder(errors)}, status_code=status_code)
