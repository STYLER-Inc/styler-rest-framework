""" Error reporting module
"""
import logging


def google_error_reporting_handler(service=None):  # pragma: no coverage
    try:
        from google.cloud import error_reporting
        client = error_reporting.Client(service=service)
        return client.report_exception

    except Exception:
        logging.warning('Could not find start error reporting client')
        return None
