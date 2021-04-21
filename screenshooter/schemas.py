from typing import Union

from pydantic import BaseModel


class BrowserSettings(BaseModel):
    width: int
    height: int
    deviceScaleFactor: Union[int, float]
    isMobile: bool
    isLandscape: bool
