""" Filter logs for health check and OpenAPI spec.
"""
import logging


class EndpointFilter(logging.Filter):  # pragma: no coverage
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        if 'GET / HTTP' in msg:  # Health check
            return False
        if 'openapi' in msg or 'docs' in msg:  # Open API Spec
            return False
        return True
