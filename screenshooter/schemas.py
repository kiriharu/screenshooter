from typing import Union, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class Viewport(BaseModel):
    width: int
    height: int
    deviceScaleFactor: Union[int, float]
    isMobile: bool
    isLandscape: bool
