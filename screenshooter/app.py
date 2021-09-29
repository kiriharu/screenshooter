import os
from functools import partial

import sentry_sdk
from fastapi import FastAPI
from pyppeteer.errors import PageError, BrowserError, NetworkError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from screenshooter.routes import main_router
from screenshooter.errors import (
    page_error_handler,
)

sentry_dsn = os.getenv("SENTRY_DSN", None)
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
app.add_exception_handler(BrowserError, page_error_handler)
app.add_exception_handler(
    NetworkError,
    partial(page_error_handler, details="Network error. Check resource or cookies")
)

app.include_router(main_router)
