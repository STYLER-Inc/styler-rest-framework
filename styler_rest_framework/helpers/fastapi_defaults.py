""" Define helper methods to reduce the boilerplate code for a server
"""

import logging

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
