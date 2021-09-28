from typing import Union, TypeVar

from pydantic import BaseModel

DataT = TypeVar('DataT')


class BrowserSettings(BaseModel):
    width: int
    height: int
    deviceScaleFactor: Union[int, float]
    isMobile: bool
    isLandscape: bool

