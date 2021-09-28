from io import BytesIO
from typing import Optional, Union

from fastapi import APIRouter, Query
from pydantic import HttpUrl
from starlette.responses import StreamingResponse

from screenshooter.schemas import BrowserSettings
from screenshooter.screenshot import Screenshot

main_router = APIRouter()


@main_router.get("/screenshot")
async def screenshoot(
    url: HttpUrl,
    width: Optional[int] = Query(800, lt=2000),
    height: Optional[int] = Query(600, lt=2000),
    isMobile: Optional[bool] = False,
    deviceScaleFactor: Optional[Union[int, float]] = 1,
    isLandscape: Optional[bool] = False,
) -> StreamingResponse:
    screenshot_obj = Screenshot(str(url), BrowserSettings(
        width=width, height=height, isMobile=isMobile,
        deviceScaleFactor=deviceScaleFactor, isLandscape=isLandscape
    ))
    async with screenshot_obj as s:
        binary = await s.get_binary_screenshot()
        return StreamingResponse(content=BytesIO(binary), media_type="image/png")