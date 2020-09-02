""" Tests for HTTP handler
"""

from unittest.mock import Mock
import json

from styler_rest_framework.services import HTTPHandler
from styler_rest_framework.exceptions.services import (
    AuthenticationError,
    AuthorizationError,
    InternalServerError,
    InvalidDataError,
    NotFoundError,
    PaymentRequiredError,
    UnexpectedError,
)
import pytest


class IdentityMock:
    """ Mock an identity instance
    """
    def token(self):
        return 'aaa.aaaaa.aaa'

    def trace_header(self):
        return {}

    def localization(self):
        return 'ja'


class TestInit:
    """ Tests for init
    """
    def test_with_identity(self):
        iden = IdentityMock()
        handler = HTTPHandler(identity=iden)

        assert 'Authorization' in handler.headers
        assert handler.headers['Authorization'] == f'Bearer {iden.token()}'

    def test_with_custom_headers(self):
        handler = HTTPHandler(
            identity=IdentityMock(),
            headers={'my-custom-header': '1234'}
        )

        assert 'my-custom-header' in handler.headers
        assert handler.headers['my-custom-header'] == '1234'


class TestPost:
    """ Test method post
    """
    async def test_post(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'POST',
            aresponses.Response(
                status=201,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        result = await handler.post(
            'https://some.url/resources',
            {'name': 'something'}
        )

        assert result == {'id': '1234'}

    test_cases = [
        (400, InvalidDataError),
        (401, AuthenticationError),
        (402, PaymentRequiredError),
        (403, AuthorizationError),
        (404, NotFoundError),
        (500, InternalServerError),
        (986, UnexpectedError),
    ]

    @pytest.mark.parametrize("status, exception", test_cases)
    async def test_error_responses(self, status, exception, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'POST',
            aresponses.Response(
                status=status,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())
        with pytest.raises(exception):
            _ = await handler.post(
                'https://some.url/resources',
                {'name': 'something'}
            )

    async def test_custom_handler(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'POST',
            aresponses.Response(
                status=402,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        with pytest.raises(ValueError):
            _ = await handler.post(
                'https://some.url/resources',
                {'name': 'something'},
                error_handlers={402: Mock(side_effect=ValueError())}
            )


class TestPut:
    """ Test method put
    """
    async def test_put(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources/1234',
            'PUT',
            aresponses.Response(
                status=200,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        result = await handler.put(
            'https://some.url/resources/1234',
            {'name': 'something'}
        )

        assert result == {'id': '1234'}

    test_cases = [
        (400, InvalidDataError),
        (401, AuthenticationError),
        (402, PaymentRequiredError),
        (403, AuthorizationError),
        (404, NotFoundError),
        (500, InternalServerError),
        (986, UnexpectedError),
    ]

    @pytest.mark.parametrize("status, exception", test_cases)
    async def test_error_responses(self, status, exception, aresponses):
        aresponses.add(
            'some.url',
            '/resources/1234',
            'PUT',
            aresponses.Response(
                status=status,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())
        with pytest.raises(exception):
            _ = await handler.put(
                'https://some.url/resources/1234',
                {'name': 'something'}
            )

    async def test_custom_handler(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources/1234',
            'PUT',
            aresponses.Response(
                status=402,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        with pytest.raises(ValueError):
            _ = await handler.put(
                'https://some.url/resources/1234',
                {'name': 'something'},
                error_handlers={402: Mock(side_effect=ValueError())}
            )


class TestPatch:
    """ Test method patch
    """
    async def test_patch(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources/1234',
            'PATCH',
            aresponses.Response(
                status=200,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        result = await handler.patch(
            'https://some.url/resources/1234',
            {'name': 'something'}
        )

        assert result == {'id': '1234'}

    test_cases = [
        (400, InvalidDataError),
        (401, AuthenticationError),
        (402, PaymentRequiredError),
        (403, AuthorizationError),
        (404, NotFoundError),
        (500, InternalServerError),
        (986, UnexpectedError),
    ]

    @pytest.mark.parametrize("status, exception", test_cases)
    async def test_error_responses(self, status, exception, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'PATCH',
            aresponses.Response(
                status=status,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())
        with pytest.raises(exception):
            _ = await handler.patch(
                'https://some.url/resources',
                {'name': 'something'}
            )

    async def test_custom_handler(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'PATCH',
            aresponses.Response(
                status=402,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        with pytest.raises(ValueError):
            _ = await handler.patch(
                'https://some.url/resources',
                {'name': 'something'},
                error_handlers={402: Mock(side_effect=ValueError())}
            )


class TestGet:
    """ Test method get
    """
    async def test_get(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'GET',
            aresponses.Response(
                status=200,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        result = await handler.get(
            'https://some.url/resources'
        )

        assert result == {'id': '1234'}

    test_cases = [
        (400, InvalidDataError),
        (401, AuthenticationError),
        (402, PaymentRequiredError),
        (403, AuthorizationError),
        (404, NotFoundError),
        (500, InternalServerError),
        (986, UnexpectedError),
    ]

    @pytest.mark.parametrize("status, exception", test_cases)
    async def test_error_responses(self, status, exception, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'GET',
            aresponses.Response(
                status=status,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())
        with pytest.raises(exception):
            _ = await handler.get(
                'https://some.url/resources'
            )

    async def test_custom_handler(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'GET',
            aresponses.Response(
                status=402,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        with pytest.raises(ValueError):
            _ = await handler.get(
                'https://some.url/resources',
                error_handlers={402: Mock(side_effect=ValueError())}
            )


class TestDelete:
    """ Test method delete
    """
    async def test_delete(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'DELETE',
            aresponses.Response(
                status=200,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        result = await handler.delete(
            'https://some.url/resources'
        )

        assert result == {'id': '1234'}

    test_cases = [
        (400, InvalidDataError),
        (401, AuthenticationError),
        (402, PaymentRequiredError),
        (403, AuthorizationError),
        (404, NotFoundError),
        (500, InternalServerError),
        (986, UnexpectedError),
    ]

    @pytest.mark.parametrize("status, exception", test_cases)
    async def test_error_responses(self, status, exception, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'DELETE',
            aresponses.Response(
                status=status,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())
        with pytest.raises(exception):
            _ = await handler.delete(
                'https://some.url/resources'
            )

    async def test_custom_handler(self, aresponses):
        aresponses.add(
            'some.url',
            '/resources',
            'DELETE',
            aresponses.Response(
                status=402,
                text=json.dumps({'id': '1234'}),
                content_type='application/json'
            )
        )
        handler = HTTPHandler(IdentityMock())

        with pytest.raises(ValueError):
            _ = await handler.delete(
                'https://some.url/resources',
                error_handlers={402: Mock(side_effect=ValueError())}
            )
