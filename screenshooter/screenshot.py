import asyncio
from enum import Enum
from typing import Optional, Any

from pyppeteer.browser import BrowserContext, Browser
from pyppeteer.page import Page

from screenshooter.schemas import Viewport
from screenshooter.config import WAIT_FOR_LOAD


class PicType(str, Enum):
    jpeg = "jpeg"
    png = "png"


def to_hashable(item: Any):
    if hasattr(item, "dict"):
        yield from to_hashable(list(sorted(item.dict().items())))
    elif isinstance(item, dict):
        yield from to_hashable(list(sorted(item.items())))
    elif isinstance(item, list):
        while item:
            yield from to_hashable(item.pop())
    else:
        yield item


def get_hash_from_args(args: dict):
    items = set()
    for v in to_hashable(list(args.values())):
        items.add(v)
    return hash(frozenset(items))


def prepare_cookies(cookies: dict[str, Any], url: str) -> list[dict[str, Any]]:
    prepared = []
    for cookie_key in cookies.keys():
        prepared.append(
            {
                'name': cookie_key,
                'value': cookies[cookie_key],
                'url': url
            }
        )
    return prepared


class Screenshot:

    def __init__(
        self,
        browser: Browser,
        url: str,
        viewport: Viewport,
        pic_type: PicType,
        enable_javascript: bool,
        cookies: dict[str, Any],
        useragent: Optional[str],
    ):

        loc = locals().copy()
        del loc['self']
        del loc['browser']

        self.browser = browser
        self.url = url
        self.viewport = viewport
        self.pic_type = pic_type
        self.enable_javascript = enable_javascript
        self.cookies = cookies
        self.context: Optional[BrowserContext]
        self.useragent = useragent

    async def __aenter__(self):
        self.context: BrowserContext = await self.browser.createIncognitoBrowserContext()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.context.close()
        if exc_val:
            raise

    async def get_page(self) -> Page:
        if not self.context:
            raise AttributeError("context not found, use with context manager")
        page = await self.context.newPage()
        if self.useragent:
            await page.setUserAgent(self.useragent)
        await page.setViewport(self.viewport.dict())
        await page.setJavaScriptEnabled(self.enable_javascript)
        await page.setCookie(*prepare_cookies(self.cookies, self.url))
        await page.goto(self.url)
        await asyncio.sleep(WAIT_FOR_LOAD)
        return page

    async def get_binary_screenshot(self) -> bytes:
        return await (
            await self.get_page()
        ).screenshot(type=self.pic_type.value)
