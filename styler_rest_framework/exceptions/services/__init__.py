""" Errors raised by service classes
"""


class ServiceError(Exception):  # pragma: no coverage
    """ Errors raised from services
    """


class InvalidDataError(ServiceError):   # pragma: no coverage
    """ Error when some fields are invalid (400 Bad request received)
    """
    def __init__(self, json_body):
        super().__init__()
        self.json_body = json_body


class AuthenticationError(ServiceError):    # pragma: no coverage
    """ Error when the service receives a 401 Unauthorized
    """


class AuthorizationError(ServiceError):  # pragma: no coverage
    """ Error when the service receives a 403 Forbidden
    """


class UnexpectedError(ServiceError):    # pragma: no coverage
    """ Error raised when the service receives an unexpected status code
    """
    def __init__(self, response):
        super().__init__()
        self.response = response
