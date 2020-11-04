""" Module for controllers
"""

import json
import logging

from aiohttp import web
from styler_rest_framework.exceptions.services import (
    AuthenticationError,
    AuthorizationError,
    InternalServerError,
    InvalidDataError,
    NotFoundError,
    PaymentRequiredError,
    UnexpectedError,
)
from styler_rest_framework.exceptions.business import (
    InternalError,
    PermissionDeniedError,
    ResourceNotFoundError,
    ValidationError,
)
from styler_rest_framework.api.request_scope import RequestScope


class BaseController:
    """ Base class for controllers
    """

    def get_identity(self, request):
        """ Get the identity of the logged user
        """
        try:
            return RequestScope.from_request(request)
        except ValueError:
            self.bad_request({'jwt': 'invalid'})

    def resp_for_creation(self, new_id):
        """ Default response for creation methods
        """
        return web.json_response({'id': new_id}, status=201)

    def response_ok(self, data):
        """ Default response for 200 OK
        """
        return web.json_response(data)

    def resp_for_listing(self, paginator, items):
        """ Default response for listings with pagination
        """
        return web.json_response({
            'items': items,
            'pagination': paginator.get_info()
        })

    def payment_required(self, code, reason):
        """ Default response for Error code 402
        """
        error = {
            'code': code,
            'reason': reason
        }
        logging.warning('Payment required error: %s', error)
        raise web.HTTPPaymentRequired(
            text=json.dumps(error),
            content_type='application/json')

    def bad_request(self, errors, code='validation_error'):
        """ Default response for Error code 400
        """
        error = {
            'code': code,
            'reason': errors
        }
        logging.warning('Bad request error: %s', error)
        raise web.HTTPBadRequest(
            text=json.dumps(error),
            content_type='application/json')

    def not_found(self, msg=''):
        """ Default response for Error code 404
        """
        logging.warning('Not found error error: %s', msg)
        raise web.HTTPNotFound(
            content_type='application/json')

    def unauthorized(self, msg=''):
        """ Default response for Error code 401
        """
        logging.warning('Unauthorized error: %s', msg)
        raise web.HTTPUnauthorized(
            content_type='application/json')

    def forbidden(self, msg=''):
        """ Default response for Error code 403
        """
        logging.warning('Forbidden error: %s', msg)
        raise web.HTTPForbidden(
            content_type='application/json')

    def internal_server_error(self, exception, msg=''):
        """ Default response for Error code 500
        """
        logging.exception('Internal Server error: %s', str(exception))
        raise web.HTTPInternalServerError(
            content_type='application/json')

    def handle_service_errors(self, ex):
        """ Default method for handling service related errors
        """
        if isinstance(ex, InvalidDataError):
            self.bad_request(ex.json_body().get('reason'))
        elif isinstance(ex, AuthenticationError):
            self.unauthorized()
        elif isinstance(ex, PaymentRequiredError):
            body = ex.json_body()
            self.payment_required(body.get('code'), body.get('reason'))
        elif isinstance(ex, AuthorizationError):
            self.forbidden()
        elif isinstance(ex, NotFoundError):
            self.not_found()
        elif isinstance(ex, InternalServerError):
            self.internal_server_error(exception=ex)
        elif isinstance(ex, UnexpectedError):
            self.internal_server_error(exception=ex)
        else:
            raise ex

    def handle_business_errors(self, ex):
        """ Default method for handling business related errors
        """
        if isinstance(ex, ValidationError):
            self.bad_request(ex.errors)
        elif isinstance(ex, PermissionDeniedError):
            self.forbidden()
        elif isinstance(ex, ResourceNotFoundError):
            self.not_found()
        elif isinstance(ex, InternalError):
            self.internal_server_error(exception=ex)
        else:
            raise ex
