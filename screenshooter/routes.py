from io import BytesIO
from typing import Optional, Union

from fastapi import APIRouter, Query, Depends
from pydantic import HttpUrl
from starlette.responses import StreamingResponse

from screenshooter.schemas import BrowserSettings
from screenshooter.di import check_restricted_urls
from screenshooter.screenshot import Screenshot, PicType

main_router = APIRouter()


@main_router.get("/screenshot")
async def screenshoot(
    url: HttpUrl = Depends(check_restricted_urls),
    pic_type: PicType = Query(PicType.jpeg),
    width: Optional[int] = Query(800, ge=800, le=2000),
    height: Optional[int] = Query(600, ge=600, le=2000),
    isMobile: Optional[bool] = False,
    deviceScaleFactor: Optional[Union[int, float]] = 1,
    isLandscape: Optional[bool] = False,
    enable_javascript: Optional[bool] = True
) -> StreamingResponse:
    browser_settings = BrowserSettings(
        width=width, height=height, isMobile=isMobile,
        deviceScaleFactor=deviceScaleFactor, isLandscape=isLandscape
    )
    screenshot_obj = Screenshot(
        str(url),
        browser_settings,
        pic_type,
        enable_javascript,
    )
    async with screenshot_obj as s:
        binary = await s.get_binary_screenshot()
        return StreamingResponse(content=BytesIO(binary), media_type=f"image/{pic_type.value}")
