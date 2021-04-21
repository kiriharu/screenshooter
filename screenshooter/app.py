from typing import Optional, Union
from io import BytesIO
import os

import sentry_sdk
from pydantic import HttpUrl
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, StreamingResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from screenshooter.screenshot import Screenshot
from screenshooter.schemas import BrowserSettings

sentry_dsn = os.getenv("SENTRY_DSN", False)
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        debug=os.getenv("DEBUG", False)
    )

app = FastAPI(
    title="screenshooter",
    debug=os.getenv("DEBUG", False),
    docs_url=os.getenv("DOCS_URL", None)
)
if sentry_dsn:
    app.add_middleware(SentryAsgiMiddleware)

# fix nginx issues
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")


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
