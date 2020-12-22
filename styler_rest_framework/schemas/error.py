""" HTTP error schemas
"""
from enum import Enum
from typing import Dict

from pydantic import BaseModel


class PaymentErrorCode(str, Enum):
    card_declined = 'card_declined'
    contact_support = 'contact_support'
    try_again = 'try_again'
    validation_error = 'validation_error'
    unsupported_card = 'unsupported_card'


class HTTP400Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 400
    """
    code: str
    reason: Dict[str, str]


class HTTP401Error(BaseModel):
    """ Returned by istio
    """


class HTTP402Error(BaseModel):
    """ Returned by istio
    """
    code: PaymentErrorCode
    reason: str


class HTTP403Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 403
    """


class HTTP404Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 404
    """


class HTTP409Error(BaseModel):
    """ Raised when handling HTTPExceptions with code 409
    """
