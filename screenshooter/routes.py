from typing import Optional, Union, Any

from fastapi import APIRouter, Query, Depends, Body, Request
from pydantic import HttpUrl
from starlette.responses import JSONResponse

from screenshooter.schemas import Viewport
from screenshooter.di import check_restricted_urls
from screenshooter.screenshot import Screenshot, PicType

main_router = APIRouter()


@main_router.post("/screenshot")
async def screenshoot(
    request: Request,
    url: HttpUrl = Depends(check_restricted_urls),
    pic_type: PicType = Query(PicType.jpeg),
    width: Optional[int] = Query(800, ge=800, le=2000),
    height: Optional[int] = Query(600, ge=600, le=2000),
    isMobile: Optional[bool] = False,
    deviceScaleFactor: Optional[Union[int, float]] = 1,
    isLandscape: Optional[bool] = False,
    enable_javascript: Optional[bool] = True,
    cookies: Optional[dict[str, Any]] = Body(default={}),
    useragent: Optional[str] = None,
) -> JSONResponse:
    browser_settings = Viewport(
        width=width,
        height=height,
        isMobile=isMobile,
        deviceScaleFactor=deviceScaleFactor,
        isLandscape=isLandscape,
    )
    screenshot_obj = Screenshot(
        request.app.state.browser,
        request.app.state.scr_cache,
        str(url),
        browser_settings,
        pic_type,
        enable_javascript,
        cookies,
        useragent,
    )
    async with screenshot_obj as s:
        path = await s.get_screenshot()
        return JSONResponse(dict(url=path[0], ttl=path[1]))
