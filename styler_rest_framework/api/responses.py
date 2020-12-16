""" Helper to build responses
"""
from typing import Dict
import logging

from styler_rest_framework.schemas.error import (
    HTTP400Error,
    HTTP401Error,
    HTTP403Error,
    HTTP404Error,
    HTTP409Error
)
from fastapi import HTTPException
from styler_rest_framework.exceptions.business import (
    PermissionDeniedError,
    ResourceNotFoundError,
    ValidationError,
    ConflictError
)


def standard(*codes) -> Dict:
    """ Generate the default configuration for error codes
    """
    codes = codes or (400, 401, 403, 404, 409)
    responses = {}
    if 400 in codes:
        responses[400] = {'model': HTTP400Error}
    if 401 in codes:
        responses[401] = {'model': HTTP401Error}
    if 403 in codes:
        responses[403] = {'model': HTTP403Error}
    if 404 in codes:
        responses[404] = {'model': HTTP404Error}
    if 409 in codes:
        responses[409] = {'model': HTTP409Error}
    return responses


def bad_request(errors: Dict[str, str]):
    """ Return HTTP 400 error
    """
    raise HTTPException(status_code=400, detail=errors)


def forbidden(msg=None):
    """ Return HTTP 403 error
    """
    msg = msg or 'Permission denied'
    raise HTTPException(status_code=403, detail=msg)


def not_found(msg=None):
    """ Return HTTP 404 error
    """
    msg = msg or 'Resource not found'
    raise HTTPException(status_code=404, detail=msg)


def unauthorized(msg=None):
    """ Return HTTP 401 error
    """
    msg = msg or 'Invalid credentials'
    raise HTTPException(status_code=401, detail=msg)


def conflict(msg=None):
    """ Return HTTP 409 error
    """
    msg = msg or 'Resource conflict'
    raise HTTPException(status_code=409, detail=msg)


def internal_server_error(exception, msg='An error has occurred'):
    """ Return HTTP 500 error
    """
    logging.exception('Internal Server error: %s', str(exception))
    raise HTTPException(status_code=500, detail=msg)


def handle_business_errors(exception: Exception) -> None:
    """ Handle standard business exceptions
    """
    if isinstance(exception, PermissionDeniedError):
        forbidden()
    elif isinstance(exception, ResourceNotFoundError):
        not_found()
    elif isinstance(exception, ValidationError):
        bad_request(exception.errors)
    elif isinstance(exception, ConflictError):
        conflict(exception.msg)
    else:
        internal_server_error(exception)
