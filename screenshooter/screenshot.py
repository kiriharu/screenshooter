import asyncio

from pyppeteer import connect
from pyppeteer.browser import BrowserContext
from pyppeteer.page import Page

from screenshooter.schemas import BrowserSettings
from screenshooter.config import CHROME_ADDRESS, WAIT_FOR_LOAD


class Screenshot:

    def __init__(self, url: str, settings: BrowserSettings):
        self.url = url
        self.settings = settings

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
            raise

    async def get_page(self) -> Page:
        page = await self.context.newPage()
        await page.goto(self.url)
        await asyncio.sleep(WAIT_FOR_LOAD)
        return page

    async def get_base64_screenshot(self) -> str:
        return await (
            await self.get_page()
        ).screenshot(encoding="base64", type="jpeg")

    async def get_binary_screenshot(self) -> bytes:
        return await (
            await self.get_page()
        ).screenshot(type="jpeg")
