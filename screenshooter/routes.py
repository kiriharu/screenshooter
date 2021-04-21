from typing import Optional, Union
from io import BytesIO

from pydantic import HttpUrl
from fastapi import Query, Request
from fastapi.responses import PlainTextResponse, StreamingResponse, Response

from screenshooter.screenshot import Screenshot
from screenshooter.schemas import BrowserSettings


async def screenshot_route(
        request: Request,
        url: HttpUrl,
        width: Optional[int] = Query(800, lt=2000),
        height: Optional[int] = Query(600, lt=2000),
        isMobile: Optional[bool] = False,
        deviceScaleFactor: Optional[Union[int, float]] = 1,
        isLandscape: Optional[bool] = False,
) -> Response:

    screenshot = Screenshot(str(url), BrowserSettings(
        width=width, height=height, isMobile=isMobile,
        deviceScaleFactor=deviceScaleFactor, isLandscape=isLandscape
    ))

    if request.url.path == "/base64":
        plaintext = await screenshot.base64()
        return PlainTextResponse(plaintext)
    if request.url.path == "/binary":
        binary = await screenshot.binary()
        return StreamingResponse(content=BytesIO(binary), media_type="image/png")