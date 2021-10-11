from enum import Enum
from typing import Union, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class ErrorType(str, Enum):
    PageError = "screenshooter.chrome.page_error"
    BrowserError = "screenshooter.chrome.browser_error"
    NetworkError = "screenshooter.chrome.network_error"
    RestrictedAddress = "screenshooter.restricted_address"
    InvalidToken = "screenshooter.invalid_token"
    TimeoutError = "screenshooter.chrome.timeout_error"


class Error(BaseModel):
    msg: str
    type: ErrorType


class Viewport(BaseModel):
    width: int
    height: int
    deviceScaleFactor: Union[int, float]
    isMobile: bool
    isLandscape: bool
