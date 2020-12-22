""" Define helper methods to reduce the boilerplate code for a server
"""

import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from styler_rest_framework import message
from styler_rest_framework.config import defaults
from styler_rest_framework.middlewares.fastapi import exception_middleware
from styler_rest_framework.logging.error_reporting import (
    google_error_reporting_handler
)


def api_error_reporting_handler(service=None):  # pragma: no coverage
    try:
        service_name = service or defaults.ERROR_HANDLER_SERVICE
        from google.cloud import error_reporting
        handler = google_error_reporting_handler(service=service_name)

        def error_handler(request, exc):
            http_context = error_reporting.HTTPContext(
                method=request.method, url=request.path)
            handler(http_context=http_context)

        return error_handler
    except Exception:
        logging.warning('Could not find start api error reporting')
        return None


def add_middlewares(
            app,
            error_handler=None,
            service=None,
            handle_exceptions_args=None
        ):
    """ Append default exception middleware

        Args:
            app: FastAPI app
            error_handler: exception handler
            service: service name
            handle_exceptions_args: dict of parameters to the middleware
    """
    handle_exceptions_args = handle_exceptions_args or {}
    error_handler = error_handler or api_error_reporting_handler(
        service=service)

    exception_middleware.add_exception_middleware(
        app, error_handler=error_handler, **handle_exceptions_args)


def setup_validation_handler(
            app,
            validation_error_code=422,
            validation_code='validation_error'):  # pragma: no coverage
    """ Set the validation error by overriding the RequestValidationError
    """
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
            request: Request, exc: RequestValidationError):
        locale = request.headers.get('Accept-Language', 'ja')
        errors = {}
        for err in exc.errors():
            field = '.'.join(err['loc'][1:]) or 'error'
            err_type = err['type'].replace('.', '_')
            errors[field] = message.get(
                f'pydantic_validation.{err_type}',
                locale=locale,
                **err.get('ctx', {})
            )

        return JSONResponse(
            status_code=validation_error_code,
            content={'code': validation_code, 'reason': errors},
        )

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=defaults.SERVICE_NAME,
            version=defaults.VERSION,
            routes=app.routes
        )
        openapi_schema['components']['schemas'].pop('ValidationError')
        openapi_schema['components']['schemas']['HTTPValidationError'] = {
            'title': 'ValidationError',
            'type': 'object',
            'properties': {
                'code': {
                    'type': 'string'
                },
                'reason': {
                    'type': 'object',
                    'additionalProperties': {
                        'type': 'string'
                    }
                }
            },
            'required': ['code', 'reason']
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi


def setup_standard_error_format(app):  # pragma: no coverage
    """ Set the validation error by overriding the HTTPException
    """
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(r: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
        )
