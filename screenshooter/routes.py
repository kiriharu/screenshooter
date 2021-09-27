from io import BytesIO
from typing import Optional, Union

from fastapi import Query, Request
from fastapi.responses import StreamingResponse, Response, JSONResponse
from pydantic import HttpUrl

from screenshooter.schemas import BrowserSettings, Base64Response, ResponseSchema
from screenshooter.screenshot import Screenshot


async def screenshot_route(
        request: Request,
        url: HttpUrl,
        width: Optional[int] = Query(800, lt=2000),
        height: Optional[int] = Query(600, lt=2000),
        isMobile: Optional[bool] = False,
        deviceScaleFactor: Optional[Union[int, float]] = 1,
        isLandscape: Optional[bool] = False,
) -> Response:
    screenshot_obj = Screenshot(str(url), BrowserSettings(
        width=width, height=height, isMobile=isMobile,
        deviceScaleFactor=deviceScaleFactor, isLandscape=isLandscape
    ))
    async with screenshot_obj as s:
        if request.url.path == "/base64":
            plaintext = await s.get_base64_screenshot()
            return JSONResponse(ResponseSchema[Base64Response](
                data=Base64Response(
                    base64=plaintext
                )
            ).dict())
        if request.url.path == "/binary":
            binary = await s.get_binary_screenshot()
            return StreamingResponse(content=BytesIO(binary), media_type="image/png")
