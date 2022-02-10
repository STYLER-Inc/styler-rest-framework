""" Tests for the exception middleware
"""
from unittest.mock import Mock, patch, AsyncMock

from styler_rest_framework.middlewares.fastapi import auth_middleware
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


class TestAddAuthMiddleware:
    """ Tests for add_auth_middleware
    """
    def test_add_auth_middleware(self):
        app = MockFastAPI()

        auth_middleware.add_auth_middleware(app, 'development')

        assert app.middleware_func is not None
        assert callable(app.middleware_func)


class TestValidateJWTException:
    """ Tests for validating JWT
    """
    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=True))
    async def test_valid_jwt(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development')
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = 'Bearer some_jwt'

        _ = await app.middleware_func(request, call_next)

        call_next.assert_called_once()

    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=True))
    async def test_valid_jwt_without_bearer(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development')
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = 'some_jwt'

        _ = await app.middleware_func(request, call_next)

        call_next.assert_called_once()

    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=True))
    async def test_missing_jwt(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development')
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = None

        response = await app.middleware_func(request, call_next)

        call_next.assert_not_called()
        assert isinstance(response, JSONResponse)
        assert response.status_code == 401

    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=False))
    async def test_invalid_jwt(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development')
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = 'Bearer some_jwt'
        
        response = await app.middleware_func(request, call_next)

        call_next.assert_not_called()
        assert isinstance(response, JSONResponse)
        assert response.status_code == 401

    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=False))
    async def test_exclude_path(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development', excludes=['/some/path'])
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = 'Bearer some_jwt'
        request.url.path = '/some/path'
        
        response = await app.middleware_func(request, call_next)

        call_next.assert_called_once()
