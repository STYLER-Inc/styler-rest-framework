""" HTTP error schemas
"""
from typing import Dict

from pydantic import BaseModel


class HTTP400Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 400
    """
    detail: Dict[str, str]


class HTTP401Error(BaseModel):
    """ Returned by istio
    """


class HTTP403Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 403
    """
    detail: str


class HTTP404Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 404
    """
    detail: str


class HTTP409Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 409
    """
    detail: str
