""" Error reporting module
"""
import logging

from styler_rest_framework.config import defaults


def google_error_reporting_handler(service=None):  # pragma: no coverage
    try:
        service_name = service or defaults.ERROR_HANDLER_SERVICE
        from google.cloud import error_reporting
        client = error_reporting.Client(service=service_name)
        return client.report_exception

    except Exception:
        logging.warning('Could not find start error reporting client')
        return None
