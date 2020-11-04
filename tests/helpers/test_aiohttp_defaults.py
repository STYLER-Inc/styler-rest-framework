""" Tests for server defaults
"""

from unittest.mock import Mock

from styler_rest_framework.helpers import aiohttp_defaults


class TestAddMiddlewares:
    def test_add_middlewares(self):
        app = Mock()
        app.middlewares = []

        aiohttp_defaults.add_middlewares(app)

        assert len(app.middlewares) == 2
        assert callable(app.middlewares[0])
        assert callable(app.middlewares[1])

    def test_add_middlewares_with_custom_error_handler(self):
        app = Mock()
        app.middlewares = []
        error_handler = Mock()

        aiohttp_defaults.add_middlewares(app, error_handler=error_handler)

        assert len(app.middlewares) == 2
        assert callable(app.middlewares[0])
        assert callable(app.middlewares[1])
