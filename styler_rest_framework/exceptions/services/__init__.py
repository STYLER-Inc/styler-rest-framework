""" Errors raised by service classes
"""

import json


class ServiceError(Exception):
    """ Errors raised from services
    """
    def __init__(self, response):
        self.response = response

    async def json_body(self):
        """ Parse the response body

            Returns the json dict or an empty dict if it fails
        """
        try:
            return json.loads(await self.response.text())
        except json.decoder.JSONDecodeError:
            return {}

    async def text(self):
        """ Returns the text from the response
        """
        return await self.response.text()

    def response_status(self):
        return self.response.status


class InvalidDataError(ServiceError):   # pragma: no coverage
    """ Error when the service returns a 400 Bad request received
    """


class AuthenticationError(ServiceError):    # pragma: no coverage
    """ Error when the service returns a 401 Unauthorized
    """


class PaymentRequiredError(ServiceError):  # pragma: no coverage
    """ Error when the service returns a 402 Forbidden
    """


class AuthorizationError(ServiceError):  # pragma: no coverage
    """ Error when the service returns a 403 Forbidden
    """


class NotFoundError(ServiceError):  # pragma: no coverage
    """ Error when the service returns a 404 Not found
    """


class InternalServerError(ServiceError):  # pragma: no coverage
    """ Error when the service returns a 500 Not found
    """


class UnexpectedError(ServiceError):    # pragma: no coverage
    """ Error raised when the service returns an unexpected status code
    """
