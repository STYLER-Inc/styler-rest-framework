""" Define helper methods to reduce the boilerplate code for a server
"""

import logging

from styler_middleware import handle_exceptions, handle_invalid_json
from styler_rest_framework.logging import setup_logging

reporting_handler = None

try:  # pragma: no coverage
    from google.cloud import error_reporting
    client = error_reporting.Client()
    reporting_handler = client.report_exception
except Exception:
    logging.warning(
        '''
        Could not find error reporting,
        please run pip install google-cloud-error-reporting
        '''
    )


def add_middlewares(app):
    """ Append default middlewares
    """
    app.middlewares.extend([
        handle_exceptions(error_handler=reporting_handler),
        handle_invalid_json()
    ])


def set_logging():  # pragma: no coverage
    setup_logging(logging.INFO)


def default_configuration(app):  # pragma: no coverage
    set_logging()
    add_middlewares(app)
