""" Tests for server defaults
"""

from unittest.mock import Mock

from styler_rest_framework.helpers import server_defaults


class TestAddMiddlewares:
    def test_add_middlewares(self):
        app = Mock()
        app.middlewares = []

        server_defaults.add_middlewares(app)

        assert len(app.middlewares) == 2
        assert callable(app.middlewares[0])
        assert callable(app.middlewares[1])
