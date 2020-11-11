""" Tests for the exception middleware
"""
from unittest.mock import Mock, patch, AsyncMock

from styler_rest_framework.middlewares.fastapi import exception_middleware
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pytest


class MockFastAPI:
    def __init__(self):
        self.middleware_func = None

    def middleware(self, middleware_type):
        def decorator(func):
            self.middleware_func = func
        return decorator


class TestAddExceptionMiddleware:
    """ Tests for add_exception_middleware
    """
    def test_add_exception_middleware(self):
        app = MockFastAPI()

        exception_middleware.add_exception_middleware(app)

        assert app.middleware_func is not None
        assert callable(app.middleware_func)


class TestHandleException:
    """ Tests for handling exceptions
    """
    @patch('logging.exception')
    async def test_handle_exception(self, logging_mocked):
        app = MockFastAPI()
        error_handler = Mock()
        exception_middleware.add_exception_middleware(
            app, error_handler=error_handler)
        call_next = AsyncMock(side_effect=Exception('Error'))
        request = Mock()

        response = await app.middleware_func(request, call_next)

        error_handler.assert_called_once()
        logging_mocked.assert_called_once()
        assert isinstance(response, JSONResponse)

    @patch('logging.exception')
    async def test_handle_exception_without_handler(self, logging_mocked):
        app = MockFastAPI()
        exception_middleware.add_exception_middleware(app)
        call_next = AsyncMock(side_effect=Exception('Error'))
        request = Mock()

        response = await app.middleware_func(request, call_next)

        logging_mocked.assert_called_once()
        assert isinstance(response, JSONResponse)

    async def test_raise_http_exception(self):
        app = MockFastAPI()
        exception_middleware.add_exception_middleware(app)
        call_next = AsyncMock(side_effect=HTTPException(status_code=400))
        request = Mock()

        with pytest.raises(HTTPException):
            _ = await app.middleware_func(request, call_next)

    async def test_no_exception(self):
        app = MockFastAPI()
        exception_middleware.add_exception_middleware(app)
        call_next = AsyncMock(return_value=JSONResponse(status_code=200))
        request = Mock()

        response = await app.middleware_func(request, call_next)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
