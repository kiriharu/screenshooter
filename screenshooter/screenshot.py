import asyncio
from enum import Enum
from typing import Optional

from pyppeteer import connect
from pyppeteer.browser import BrowserContext
from pyppeteer.page import Page

from screenshooter.schemas import BrowserSettings
from screenshooter.config import CHROME_ADDRESS, WAIT_FOR_LOAD


class PicType(str, Enum):
    jpeg = "jpeg"
    png = "png"


class Screenshot:

    def __init__(
        self,
        url: str,
        settings: BrowserSettings,
        pic_type: PicType,
        enable_javascript: bool,
    ):
        self.url = url
        self.settings = settings
        self.pic_type = pic_type
        self.enable_javascript = enable_javascript
        self.context: Optional[BrowserContext]

    async def __aenter__(self):
        browser = await connect(
            browserURL=CHROME_ADDRESS,
            **dict(defaultViewport=self.settings.dict())
        )
        self.context: BrowserContext = await browser.createIncognitoBrowserContext()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.context.close()
        if exc_val:
            raise ValueError

    async def get_page(self) -> Page:
        if not self.context:
            raise AttributeError("context not found, use with context manager")
        page = await self.context.newPage()
        await page.setJavaScriptEnabled(self.enable_javascript)
        await page.goto(self.url)
        await asyncio.sleep(WAIT_FOR_LOAD)
        return page

    async def get_binary_screenshot(self) -> bytes:
        return await (
            await self.get_page()
        ).screenshot(type=self.pic_type.value)
