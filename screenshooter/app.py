import os

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pyppeteer.errors import PageError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette.exceptions import HTTPException

from screenshooter.routes import screenshot_route
from screenshooter.errors import page_error_handler, http_exception_handler
from screenshooter.schemas import Base64Response, ResponseSchema

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
    redoc_url=os.getenv("REDOCK_URL", None),
    docs_url=os.getenv("DOCS_URL", None),
)
if sentry_dsn:
    app.add_middleware(SentryAsgiMiddleware)

# fix nginx issues
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

app.add_exception_handler(PageError, page_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_api_route(
    "/base64", screenshot_route,
    response_class=JSONResponse,
    response_model=ResponseSchema[Base64Response]
)
app.add_api_route("/binary", screenshot_route, response_class=StreamingResponse)
