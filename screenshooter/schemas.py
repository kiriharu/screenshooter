from enum import Enum
from typing import Union, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class ErrorType(str, Enum):
    PageError = "screenshooter.chrome.page_error"
    BrowserError = "screenshooter.chrome.page_error"
    NetworkError = "screenshooter.chrome.network_error"


class Error(BaseModel):
    msg: str
    type: ErrorType


class Viewport(BaseModel):
    width: int
    height: int
    deviceScaleFactor: Union[int, float]
    isMobile: bool
    isLandscape: bool
