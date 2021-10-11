import os
import glob

from pathlib import Path

import sentry_sdk
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pyppeteer import connect
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
from screenshooter.errors import add_exception_handlers
from screenshooter.di import verify_token

sentry_dsn = os.getenv("SENTRY_DSN", None)
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn, traces_sample_rate=1.0, debug=os.getenv("DEBUG", False)
    )

app = FastAPI(
    title="screenshooter",
    debug=bool(int(os.getenv("DEBUG", False))),
    redoc_url=os.getenv("REDOCK_URL", None),
    docs_url=os.getenv("DOCS_URL", None),
    dependencies=[Depends(verify_token)]
)
if sentry_dsn:
    app.add_middleware(SentryAsgiMiddleware)

# fix nginx issues
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
add_exception_handlers(app)


@app.on_event("startup")
async def on_startup():
    browser = await connect(browserURL=CHROME_ADDRESS)
    app.state.browser = browser
    cache = Cache(SCREENSHOT_CACHE_TTL)
    app.state.scr_cache = cache
    # remove data in SCREENSHOTS_DIR
    for file in glob.glob(os.path.join(SCREENSHOTS_DIR, "*")):
        os.remove(file)

Path(SCREENSHOTS_DIR).mkdir(parents=True, exist_ok=True)  # ensure dir exists
app.include_router(main_router)
app.mount(
    f"/{SCREENSHOTS_STATIC_DIR}",
    StaticFiles(directory=SCREENSHOTS_STATIC_DIR),
    name=SCREENSHOTS_STATIC_DIR,
)

