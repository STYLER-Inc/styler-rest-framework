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
    ValidationError,
    ResourceNotFoundError,
    PermissionDeniedError
)
from styler_rest_framework.controllers.request_scope import RequestScope


class BaseController:
    """ Base class for controllers
    """

    def get_identity(self, request):
        """ Get the identity of the logged user
        """
        try:
            return RequestScope(request)
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
        logging.error('Payment required error: %s', error)
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
        logging.error('Bad request error: %s', error)
        raise web.HTTPBadRequest(
            text=json.dumps(error),
            content_type='application/json')

    def not_found(self, msg=''):
        """ Default response for Error code 404
        """
        logging.error('Not found error error: %s', msg)
        raise web.HTTPNotFound(
            content_type='application/json')

    def unauthorized(self, msg=''):
        """ Default response for Error code 401
        """
        logging.error('Unauthorized error: %s', msg)
        raise web.HTTPUnauthorized(
            content_type='application/json')

    def forbidden(self, msg=''):
        """ Default response for Error code 403
        """
        logging.error('Forbidden error: %s', msg)
        raise web.HTTPForbidden(
            content_type='application/json')

    async def handle_service_errors(self, ex):
        """ Default method for handling service related errors
        """
        if isinstance(ex, InvalidDataError):
            data = await ex.json_body()
            print(data)
            self.bad_request(data.get('reason'))
        elif isinstance(ex, AuthenticationError):
            self.unauthorized()
        elif isinstance(ex, PaymentRequiredError):
            body = await ex.json_body()
            self.payment_required(body.get('code'), body.get('reason'))
        elif isinstance(ex, AuthorizationError):
            self.forbidden()
        elif isinstance(ex, NotFoundError):
            self.not_found()
        elif isinstance(ex, InternalServerError):
            raise web.HTTPInternalServerError() from ex
        elif isinstance(ex, UnexpectedError):
            raise web.HTTPInternalServerError() from ex
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
        else:
            raise ex
