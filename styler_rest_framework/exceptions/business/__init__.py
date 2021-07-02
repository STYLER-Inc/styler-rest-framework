""" Errors raised by business classes
"""


class BusinessError(Exception):  # pragma: no coverage
    """Error raised from business classes"""


class InternalError(BusinessError):  # pragma: no coverage
    """Error raised when an unexpected error occurs"""


class PermissionDeniedError(BusinessError):  # pragma: no coverage
    """Error raised when the user has no access to the resource"""


class ResourceNotFoundError(BusinessError):  # pragma: no coverage
    """Error raised when the required resource was not found"""


class ValidationError(BusinessError):  # pragma: no coverage
    """Error raised when there is a validation error"""

    def __init__(self, errors):
        super().__init__()
        self.errors = errors


class ConflictError(BusinessError):
    """Error raised when request could not be completed due to a conflict
    with the current state of the resource
    """

    def __init__(self, msg):
        super().__init__()
        self.msg = msg
