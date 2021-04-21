from typing import Optional, Union
from io import BytesIO
import os

import sentry_sdk
from pydantic import HttpUrl
from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse, StreamingResponse, Response
from pyppeteer.errors import PageError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from screenshooter.screenshot import Screenshot
from screenshooter.schemas import BrowserSettings

from screenshooter.errors import page_error_handler

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


app.add_exception_handler(PageError, page_error_handler)
app.add_api_route("/base64", screenshot_route, response_class=PlainTextResponse)
app.add_api_route("/binary", screenshot_route, response_class=StreamingResponse)
