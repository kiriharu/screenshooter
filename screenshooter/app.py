import os
import glob
from functools import partial
from pathlib import Path

import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pyppeteer import connect
from pyppeteer.errors import PageError, BrowserError, NetworkError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from screenshooter.cache import Cache
from screenshooter.config import (
    CHROME_ADDRESS,
    SCREENSHOT_CACHE_TTL,
    SCREENSHOTS_STATIC_DIR,
    SCREENSHOTS_DIR,
)
from screenshooter.routes import main_router
from screenshooter.errors import (
    page_error_handler,
)

sentry_dsn = os.getenv("SENTRY_DSN", None)
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn, traces_sample_rate=1.0, debug=os.getenv("DEBUG", False)
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
    partial(page_error_handler, details="Network error. Check resource or cookies"),
)


@app.on_event("startup")
async def on_startup():
    browser = await connect(browserURL=CHROME_ADDRESS)
    app.state.browser = browser
    cache = Cache(SCREENSHOT_CACHE_TTL)
    app.state.scr_cache = cache
    # remove data in SCREENSHOTS_DIR
    Path(SCREENSHOTS_DIR).mkdir(parents=True, exist_ok=True)  # ensure dir exists
    for file in glob.glob(os.path.join(SCREENSHOTS_DIR, "*")):
        os.remove(file)


app.include_router(main_router)
app.mount(
    f"/{SCREENSHOTS_STATIC_DIR}",
    StaticFiles(directory=SCREENSHOTS_STATIC_DIR),
    name=SCREENSHOTS_STATIC_DIR,
)
