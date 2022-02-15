""" Tests for AIOHTTP auth middleware.
"""

from json.decoder import JSONDecodeError
from unittest.mock import AsyncMock, Mock, patch
import asyncio

from aiohttp.web import HTTPException
from styler_rest_framework.middlewares.aiohttp.auth_middleware import add_auth_middleware
import pytest



def test_generator():
    mid = add_auth_middleware('development')

    assert callable(mid)


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=True))
def test_normal_flow():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer token'
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware('development')

    resp = asyncio.run(middleware(request, handler))

    assert resp == 'response'


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=False))
def test_exclude_path():
    request = Mock()
    request.path = '/some/path'
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware('development', excludes=['/some/path'])

    resp = asyncio.run(middleware(request, handler))

    assert resp == 'response'


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=False))
def test_missing_jwt():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = None
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware('development')

    resp = asyncio.run(middleware(request, handler))

    assert resp.status == 401


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=False))
def test_invalid_jwt():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer some-invalid-token'
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware('development')

    resp = asyncio.run(middleware(request, handler))

    assert resp.status == 401


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=True))
def test_pass_exceptions():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer token'
    handler = AsyncMock(side_effect=ValueError('invalid something'))
    middleware = add_auth_middleware('development')

    with pytest.raises(ValueError):
        _ = asyncio.run(middleware(request, handler))


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=True))
def test_pass_http_exceptions():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer token'
    handler = AsyncMock(side_effect=HTTPException())
    middleware = add_auth_middleware('development')

    with pytest.raises(HTTPException):
        _ = asyncio.run(middleware(request, handler))
