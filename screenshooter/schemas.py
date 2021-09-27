from typing import Union, Optional, TypeVar, Generic
from enum import Enum

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class Error(str, Enum):
    NotResolved = "request.not_resolved"
    HTTPException = "http.exception"
    UnprocessableEntity = "http.unprocessable_entity"


class ErrorResponse(BaseModel):
    msg: str
    code: Error


class ResponseSchema(GenericModel, Generic[DataT]):
    success: bool = True
    data: Optional[DataT]
    error: Optional[ErrorResponse]


class Base64Response(BaseModel):
    base64: str


class BrowserSettings(BaseModel):
    width: int
    height: int
    deviceScaleFactor: Union[int, float]
    isMobile: bool
    isLandscape: bool

