""" Configures logging with stackdriver
"""

import logging

import google.cloud.logging


def setup_logging(level=logging.INFO):  # pragma: no coverage
    """ Setup logging
    """
    client = google.cloud.logging.Client()
    excluded_logger_defaults = (
        "google.cloud",
        "google.auth",
        "google_auth_httplib2"
    )

    # don't propagate excluded loggers (and don't send them to stderr either)
    for logger_name in excluded_logger_defaults:
        logging.getLogger(logger_name).propagate = False
        logging.getLogger(logger_name).addHandler(logging.NullHandler())

    handler = client.get_default_handler()
    handler.setLevel(level)
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level)
