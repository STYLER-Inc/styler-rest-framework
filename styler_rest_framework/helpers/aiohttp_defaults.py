""" Define helper methods to reduce the boilerplate code for a server
"""

import logging

from styler_middleware import handle_exceptions, handle_invalid_json
from styler_rest_framework.logging import setup_logging


def google_error_reporting_handler():  # pragma: no coverage
    try:
        from google.cloud import error_reporting
        client = error_reporting.Client()

        def error_handler(request, exc):
            client.report_exception

        return error_handler
    except Exception:
        logging.warning(
            '''
            Could not find error reporting,
            please run pip install google-cloud-error-reporting
            '''
        )
        return None


def add_middlewares(app, error_handler=None):
    """ Append default middlewares
    """
    if not error_handler:
        error_handler = google_error_reporting_handler()
    app.middlewares.extend([
        handle_exceptions(error_handler=error_handler),
        handle_invalid_json()
    ])


def set_logging(level=logging.INFO):  # pragma: no coverage
    setup_logging(level)


def default_configuration(app):  # pragma: no coverage
    set_logging()
    add_middlewares(app)
