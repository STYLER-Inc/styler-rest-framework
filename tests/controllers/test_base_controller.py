""" Tests for the base controller
"""

from unittest.mock import MagicMock, Mock, patch
import json

from aiohttp import web
from styler_rest_framework.controllers import \
    BaseController, get_token_auth_header
from styler_rest_framework.exceptions.services import (
    AuthenticationError,
    AuthorizationError,
    InternalServerError,
    InvalidDataError,
    NotFoundError,
    PaymentRequiredError,
    UnexpectedError,
)
from styler_rest_framework.exceptions.business import \
    ValidationError, ResourceNotFoundError, PermissionDeniedError
from styler_identity import Identity
import pytest


class TestResponses:
    """ Tests for responses
    """
    @patch('aiohttp.web.json_response')
    def test_resp_for_creation(self, mocked_resp):
        """ HTTP 201 with new id
        """
        base = BaseController()
        mocked_resp.return_value = 'abc'

        resp = base.resp_for_creation('abc')

        assert resp == 'abc'
        mocked_resp.assert_called_with({'id': 'abc'}, status=201)

    @patch('aiohttp.web.json_response')
    def test_response_ok(self, mocked_resp):
        """ Default HTTP 200 with data
        """
        base = BaseController()
        mocked_resp.return_value = 'abc'

        resp = base.response_ok('abc')

        assert resp == 'abc'
        mocked_resp.assert_called_with('abc')

    @patch('aiohttp.web.json_response')
    def test_resp_for_listing(self, mocked_resp):
        """ Default HTTP 200 with list
        """
        base = BaseController()
        paginator = Mock()
        paginator.get_info.return_value = 'aaa'
        mocked_resp.return_value = 'abc'

        resp = base.resp_for_listing(paginator, ['1234'])

        assert resp == 'abc'
        mocked_resp.assert_called_with({
            'items': ['1234'],
            'pagination': 'aaa'
        })

    @patch('logging.error')
    def test_bad_request(self, mocked_logger):
        """ Default HTTP 400 with errors
        """
        base = BaseController()
        errors = {
            'error': 'general error'
        }

        with pytest.raises(web.HTTPBadRequest) as expected:
            base.bad_request(errors)
        mocked_logger.assert_called_once()
        resp = json.loads(expected.value.text)
        assert resp['reason'] == errors

    @patch('logging.error')
    def test_not_found(self, mocked_logger):
        """ Default HTTP 404 with errors
        """
        base = BaseController()

        with pytest.raises(web.HTTPNotFound) as expected:
            base.not_found()
        mocked_logger.assert_called_once()
        assert expected.value.status == 404

    @patch('logging.error')
    def test_forbidden(self, mocked_logger):
        """ Default HTTP 403 with errors
        """
        base = BaseController()

        with pytest.raises(web.HTTPForbidden) as expected:
            base.forbidden()
        mocked_logger.assert_called_once()
        assert expected.value.status == 403

    @patch('logging.error')
    def test_unauthorized(self, mocked_logger):
        """ Default HTTP 401 with errors
        """
        base = BaseController()

        with pytest.raises(web.HTTPUnauthorized) as expected:
            base.unauthorized()
        mocked_logger.assert_called_once()
        assert expected.value.status == 401

    @patch('logging.error')
    def test_payment_required(self, mocked_logger):
        """ Default HTTP 402 with errors
        """
        base = BaseController()

        with pytest.raises(web.HTTPPaymentRequired) as expected:
            base.payment_required(code='aaa', reason='bbb')
        mocked_logger.assert_called_once()
        assert expected.value.status == 402


class MockResponse:
    def __init__(self, text, status):
        self.body_text = text
        self.status = status

    async def text(self):
        return self.body_text


class TestHandleServiceErrors:
    """ Tests for handle_service_errors
    """
    async def test_invalid_data(self):
        base = BaseController()
        base.bad_request = MagicMock('aaa')
        error = {
            'code': 'some_code',
            'reason': {'error': 'something'}
        }
        response = MockResponse(json.dumps(error), 400)

        await base.handle_service_errors(InvalidDataError(response))

        base.bad_request.assert_called_with({'error': 'something'})

    async def test_authentication_error(self):
        base = BaseController()
        base.unauthorized = MagicMock('aaa')
        response = MockResponse('Unauthorized', 401)

        await base.handle_service_errors(AuthenticationError(response))

        base.unauthorized.assert_called_with()

    async def test_payment_required_error(self):
        base = BaseController()
        base.payment_required = MagicMock('aaa')
        error = {
            'code': 'some_code',
            'reason': {'error': 'something'}
        }
        response = MockResponse(json.dumps(error), 402)

        await base.handle_service_errors(PaymentRequiredError(response))

        base.payment_required.assert_called_with(
            'some_code', {'error': 'something'})

    async def test_authorization_error(self):
        base = BaseController()
        base.forbidden = MagicMock('aaa')
        response = MockResponse('Forbidden', 403)

        await base.handle_service_errors(AuthorizationError(response))

        base.forbidden.assert_called_with()

    async def test_not_found_error(self):
        base = BaseController()
        base.not_found = MagicMock('aaa')
        response = MockResponse('Not found', 404)

        await base.handle_service_errors(NotFoundError(response))

        base.not_found.assert_called_with()

    async def test_internal_server_error(self):
        base = BaseController()
        response = MockResponse('Error', 500)

        with pytest.raises(web.HTTPInternalServerError):
            await base.handle_service_errors(InternalServerError(response))

    async def test_unexpected_error(self):
        base = BaseController()

        with pytest.raises(web.HTTPInternalServerError):
            await base.handle_service_errors(UnexpectedError(Mock()))

    async def test_other_exceptions_error(self):
        base = BaseController()

        with pytest.raises(ValueError):
            await base.handle_service_errors(ValueError())


class TestHandleBusinessErrors:
    """ Tests for handle_business_errors
    """
    def test_invalid_data(self):
        base = BaseController()
        base.bad_request = MagicMock('aaa')
        error = {'field': 'invalid'}

        base.handle_business_errors(ValidationError(error))

        base.bad_request.assert_called_with({'field': 'invalid'})

    def test_forbidden_error(self):
        base = BaseController()
        base.forbidden = MagicMock('aaa')

        base.handle_business_errors(PermissionDeniedError())

        base.forbidden.assert_called_with()

    def test_not_found_error(self):
        base = BaseController()
        base.not_found = MagicMock('aaa')

        base.handle_business_errors(ResourceNotFoundError())

        base.not_found.assert_called_with()

    def test_other_exceptions_error(self):
        base = BaseController()

        with pytest.raises(ValueError):
            base.handle_business_errors(ValueError())


class TestGetTokenAuthHeader:
    """ Tests for get_token_auth_header
    """
    def test_get_token(self):
        """ Should return the token
        """
        request = Mock()
        request.headers.get.return_value = 'Bearer TOKEN'

        token = get_token_auth_header(request)

        assert token == 'TOKEN'

    def test_without_header(self):
        """ Should raise an exception if there is no Authorization header
        """
        request = Mock()
        request.headers.get.return_value = None

        with pytest.raises(ValueError) as expected:
            get_token_auth_header(request)
        assert str(expected.value) == 'Authorization header is expected'

    def test_without_bearer(self):
        """ Should raise an exception if there is no bearer
        """
        request = Mock()
        request.headers.get.return_value = 'token TOKEN'

        with pytest.raises(ValueError) as expected:
            get_token_auth_header(request)
        assert str(expected.value) == \
            'Authorization header must start with Bearer'

    def test_without_token(self):
        """ Should raise an exception if the auth is invalid
        """
        request = Mock()
        request.headers.get.return_value = 'Bearer'

        with pytest.raises(ValueError) as expected:
            get_token_auth_header(request)
        assert str(expected.value) == 'Token not found'

    def test_invalid_auth(self):
        """ Should raise an exception if the Authorization is invalid
        """
        request = Mock()
        request.headers.get.return_value = 'Bearer TOKEN TOKEN'

        with pytest.raises(ValueError) as expected:
            get_token_auth_header(request)
        assert str(expected.value) == \
            'Authorization header must be Bearer token'


class TestGetIdentity:
    """ Tests for BaseController.get_identity
    """
    custom_token = (
        'eyJhbGciOiJSUzI1NiIsImtpZCI6ImMzZjI3NjU0MmJmZmU0NWU5OG'
        'MyMGQ2MDNlYmUyYmExMTc2ZWRhMzMiLCJ0eXAiOiJKV1QifQ.eyJzeXN0ZW1fYWRta'
        'W4iOmZhbHNlLCJjbGFpbXMiOnsic2hvcHMiOlsiN2YwNzZjNDgtMGU0Yy00MDQ0LTl'
        'kNDctMjM0MjM0MzI0MjM0IiwiN2YwNzZjNDgtMGU0Yy00MDQ0LTlkNDctMzg4OTk5M'
        'Dk4MDkwIl0sIm9yZ2FuaXphdGlvbnMiOltdfSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV'
        '0b2tlbi5nb29nbGUuY29tL2ZhY3ktZGV2ZWxvcG1lbnQiLCJhdWQiOiJmYWN5LWRld'
        'mVsb3BtZW50IiwiYXV0aF90aW1lIjoxNTkyODg2Mjg5LCJ1c2VyX2lkIjoiNm5hZjg'
        'wanR5YlZSdVAyMmVZY0lZR1gyS0pLMiIsInN1YiI6IjZuYWY4MGp0eWJWUnVQMjJlW'
        'WNJWUdYMktKSzIiLCJpYXQiOjE1OTI4ODYyODksImV4cCI6MTU5Mjg4OTg4OSwiZW1'
        'haWwiOiJicnVuby5zdWdhbm9Ac3R5bGVyLmxpbmsiLCJlbWFpbF92ZXJpZmllZCI6Z'
        'mFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYnJ1bm8uc3V'
        'nYW5vQHN0eWxlci5saW5rIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.'
        'VNJtVQ9nmvbpUkMM95cdN06O3NDUqdBwEgmczfWKR2Vt5fOFQGtFykEovEmajdVHZO'
        'm4tbJlbfoILu0i_GsO-7jaoYNBOC9-tIBiD8pvUCeL4iQj2jhpvR6z3PEtTyA7i7Ae'
        'VUj9wuxrzYm0wtcLTR1vSEp4jTj3Nw5KD4adPq4IF63SKqywNLkmgURuQnF-WlaZBn'
        'g2CK0AMddY0Qt-1Z0IFUp-i_tXkGMOPBjXswq1kPxyZ2xtNWZjQZ5sWNw2dmkC2wyf'
        'EmnQ5Zm9UJvrS6tiCigTGkF43PhwTl26K9ztwOtekrpOiwap-c55rUG8TbobpmGGkF'
        'i9Q3r5dHH-ag'
    )

    def test_get_identity(self):
        request = Mock()
        request.headers.get.return_value = f'Bearer {self.custom_token}'
        contr = BaseController()

        identity = contr.get_identity(request)

        assert isinstance(identity, Identity)

    def test_invalid_jwt(self):
        request = Mock()
        request.headers.get.return_value = 'Bearer aa.aa.aa'
        contr = BaseController()
        contr.bad_request = MagicMock()

        _ = contr.get_identity(request)

        contr.bad_request.assert_called_once()
