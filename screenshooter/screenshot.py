from pyppeteer import launch
from pyppeteer.page import Page

from screenshooter.schemas import BrowserSettings


class Screenshot:

    def __init__(self, url: str, settings: BrowserSettings):
        self.url = url
        self.settings = settings

    async def page(self) -> Page:
        browser = await launch(
            options=dict(defaultViewport=self.settings.dict())
        )
        page = await browser.newPage()
        await page.goto(self.url)
        return page

    async def base64(self) -> str:
        page = await self.page()
        return await page.screenshot(encoding="base64")

    async def binary(self) -> bytes:
        page = await self.page()
        return await page.screenshot()
