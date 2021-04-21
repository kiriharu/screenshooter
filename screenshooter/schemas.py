from typing import Union, Optional
from enum import Enum

from pydantic import BaseModel


class Error(str, Enum):
    NotResolved = "not_resolved_error"


class BrowserSettings(BaseModel):
    width: int
    height: int
    deviceScaleFactor: Union[int, float]
    isMobile: bool
    isLandscape: bool


class ErrorResponse(BaseModel):
    msg: str
    type: Error
    detail: Optional[dict] = None
