""" Tests for AIOHTTP auth middleware.
"""

from json.decoder import JSONDecodeError
from unittest.mock import AsyncMock, Mock, patch
import asyncio

from aiohttp.web import HTTPException
from styler_rest_framework.middlewares.aiohttp.auth_middleware import add_auth_middleware
import pytest



def test_generator():
    mid = add_auth_middleware(Mock(), 'development')

    assert callable(mid)


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=True))
def test_normal_flow():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer token'
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware(Mock(), 'development')

    resp = asyncio.run(middleware(request, handler))

    assert resp == 'response'


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=False))
def test_exclude_path():
    request = Mock()
    request.path = '/some/path'
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware(Mock(), 'development', excludes=['/some/path'])

    resp = asyncio.run(middleware(request, handler))

    assert resp == 'response'

cases = [
    ('/some/path/f1225763-3eef-4067-b1ab-17d99b126eab/something', True),
    ('/some/path/f1225763-3eef-4067-b1ab-17d99b126eab/something/', True),
    ('/some/path/something', False),
    ('/some/path', False),
    ('/some/path//something', False),
    ('/some/path/1234/1234/something', False),
    ('/path/1234/something', False),
]
@pytest.mark.parametrize('path, expected', cases)
@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=False))
def test_exclude_regex_path(path, expected):
    request = Mock()
    request.path = path
    request.headers = Mock()
    request.headers.get.return_value = 'bearer token'
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware(Mock(), 'development', excludes_regex=['^/some/path/(\w|\d|-)+/something/?$'])

    resp = asyncio.run(middleware(request, handler))

    assert expected == (resp == 'response')


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=False))
def test_missing_jwt():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = None
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware(Mock(), 'development')

    resp = asyncio.run(middleware(request, handler))

    assert resp.status == 401


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=False))
def test_invalid_jwt():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer some-invalid-token'
    handler = AsyncMock(return_value='response')
    middleware = add_auth_middleware(Mock(), 'development')

    resp = asyncio.run(middleware(request, handler))

    assert resp.status == 401


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=True))
def test_pass_exceptions():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer token'
    handler = AsyncMock(side_effect=ValueError('invalid something'))
    middleware = add_auth_middleware(Mock(), 'development')

    with pytest.raises(ValueError):
        _ = asyncio.run(middleware(request, handler))


@patch('styler_rest_framework.middlewares.aiohttp.auth_middleware.validate', Mock(return_value=True))
def test_pass_http_exceptions():
    request = Mock()
    request.path = '/some/path'
    request.headers = Mock()
    request.headers.get.return_value = 'bearer token'
    handler = AsyncMock(side_effect=HTTPException())
    middleware = add_auth_middleware(Mock(), 'development')

    with pytest.raises(HTTPException):
        _ = asyncio.run(middleware(request, handler))
