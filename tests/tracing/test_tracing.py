""" Tests for tracing
"""

from unittest.mock import MagicMock

from styler_rest_framework.tracing import config_tracer


def test_middleware():
    app = MagicMock()

    config_tracer(app, 'MyProject')

    app.middlewares.append.assert_called_once()
