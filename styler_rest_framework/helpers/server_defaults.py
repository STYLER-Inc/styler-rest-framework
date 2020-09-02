""" Define helper methods to reduce the boilerplate code for a server
"""

import logging

from styler_middleware import handle_exceptions, handle_invalid_json
from styler_rest_framework.logging import setup_logging


def add_middlewares(app):
    """ Append default middlewares
    """
    app.middlewares.extend([handle_exceptions(), handle_invalid_json()])


def set_logging():  # pragma: no coverage
    setup_logging(logging.INFO)


def default_configuration(app):  # pragma: no coverage
    set_logging()
    add_middlewares(app)
