""" Tests for server defaults
"""

from unittest.mock import Mock

from styler_rest_framework.helpers import fastapi_defaults


class MockFastAPI:
    def __init__(self):
        self.middleware_func = None

    def middleware(self, middleware_type):
        def decorator(func):
            self.middleware_func = func
        return decorator


class TestAddMiddlewares:
    def test_add_middlewares(self):
        app = MockFastAPI()

        fastapi_defaults.add_middlewares(app)

        assert app.middleware_func is not None
        assert callable(app.middleware_func)

    def test_add_middlewares_with_custom_error_handler(self):
        app = MockFastAPI()
        error_handler = Mock()

        fastapi_defaults.add_middlewares(app, error_handler=error_handler)

        assert app.middleware_func is not None
        assert callable(app.middleware_func)
