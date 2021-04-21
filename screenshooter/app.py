from typing import Optional, Union
from io import BytesIO
import os

from pydantic import HttpUrl
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, StreamingResponse

from screenshooter.screenshot import Screenshot
from screenshooter.schemas import BrowserSettings


app = FastAPI(docs_url=os.getenv("DOCS_URL", None))


@app.get("/base64", response_class=PlainTextResponse)
async def base64(
        url: HttpUrl,
        width: Optional[int] = 800,
        height: Optional[int] = 600,
        isMobile: Optional[bool] = False,
        deviceScaleFactor: Optional[Union[int, float]] = 1,
        isLandscape: Optional[bool] = False,
) -> PlainTextResponse:
    screenshot = Screenshot(str(url), BrowserSettings(
        width=width, height=height, isMobile=isMobile,
        deviceScaleFactor=deviceScaleFactor, isLandscape=isLandscape
    ))
    plaintext = await screenshot.base64()
    return PlainTextResponse(plaintext)


@app.get("/binary", response_class=StreamingResponse)
async def file(
        url: HttpUrl,
        width: Optional[int] = 800,
        height: Optional[int] = 600,
        isMobile: Optional[bool] = False,
        deviceScaleFactor: Optional[Union[int, float]] = 1,
        isLandscape: Optional[bool] = False,
) -> StreamingResponse:
    screenshot = Screenshot(str(url), BrowserSettings(
        width=width, height=height, isMobile=isMobile,
        deviceScaleFactor=deviceScaleFactor, isLandscape=isLandscape
    ))
    binary = await screenshot.binary()
    return StreamingResponse(content=BytesIO(binary), media_type="image/png")
