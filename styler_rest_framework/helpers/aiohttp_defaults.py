""" Define helper methods to reduce the boilerplate code for a server
"""

import logging

from styler_middleware import handle_exceptions, handle_invalid_json
from styler_rest_framework.config import defaults
from styler_rest_framework.logging import setup_logging
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
            handle_exceptions_args=None,
            handle_invalid_json_args=None
        ):
    """ Append default middlewares
    """
    handle_exceptions_args = handle_exceptions_args or {}
    handle_invalid_json_args = handle_invalid_json_args or {}
    error_handler = error_handler or api_error_reporting_handler(
        service=service)
    app.middlewares.extend([
        handle_exceptions(
            error_handler=error_handler,
            **handle_exceptions_args
        ),
        handle_invalid_json(**handle_invalid_json_args)
    ])


def set_logging(level=logging.INFO):  # pragma: no coverage
    setup_logging(level)


def default_configuration(app):  # pragma: no coverage
    set_logging()
    add_middlewares(app)
