""" Define helper methods to reduce the boilerplate code for a server
"""

from styler_middleware import handle_exceptions, handle_invalid_json


def add_middlewares(app):
    """ Append default middlewares
    """
    app.middlewares.extend([handle_exceptions(), handle_invalid_json()])
