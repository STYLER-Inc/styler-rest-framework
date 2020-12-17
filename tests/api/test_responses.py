""" Tests for responses
"""
from unittest.mock import patch
import json

from styler_rest_framework.api import responses
from fastapi import HTTPException
from styler_rest_framework.exceptions.business import (
    InternalError,
    PermissionDeniedError,
    ResourceNotFoundError,
    ValidationError,
    ConflictError
)
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


class TestStandard:
    """ Tests for method standard
    """
    def test_include_all_standard_codes(self):
        result = responses.standard()

        assert all([code in result for code in (400, 401, 403, 404, 409)])

    def test_include_none_if_invalid_code(self):
        result = responses.standard(486)

        assert all([code not in result for code in (400, 401, 403, 404, 409)])

    def test_include_only_desired_codes(self):
        result = responses.standard(401, 404)

        assert all([code in result for code in (401, 404)])
        assert all([code not in result for code in (400, 403, 409)])


class TestResponses:
    """ Tests for response handlers
    """

    cases = [
        (responses.unauthorized, 401),
        (responses.forbidden, 403),
        (responses.not_found, 404),
        (responses.conflict, 409)
    ]

    @pytest.mark.parametrize('method,expected', cases)
    def test_raises_http_exception(self, method, expected):
        with pytest.raises(HTTPException) as exp:
            method()

        assert exp.value.status_code == expected

    def test_bad_request(self):
        with pytest.raises(HTTPException) as exp:
            responses.bad_request({'error': 'my error'})

        assert exp.value.status_code == 400
        assert exp.value.detail == {'error': 'my error'}

    def test_payment_required(self):
        with pytest.raises(HTTPException) as exp:
            responses.payment_required(
                code='card_declined', reason='something bad')

        assert exp.value.status_code == 402
        assert exp.value.detail == {
            'code': 'card_declined',
            'reason': 'something bad'
        }

    @patch('logging.exception')
    def test_internal_server_error(self, mock_log):
        with pytest.raises(HTTPException) as exp:
            responses.internal_server_error(ValueError('some msg'))

        assert exp.value.status_code == 500
        mock_log.assert_called_once()


class TestHandleBusinessErrors:
    """ Tests for handle_business_errors
    """
    cases = [
        (InternalError, None, responses.internal_server_error),
        (ValidationError, {'error': 'something'},  responses.bad_request),
        (PermissionDeniedError, None,  responses.forbidden),
        (ResourceNotFoundError, None,  responses.not_found),
        (ConflictError, 'conflict',  responses.conflict),
    ]

    @pytest.mark.parametrize('exp_type,args,expected', cases)
    def test_handle_errors(self, exp_type, args, expected):
        with patch(
            f'styler_rest_framework.api.responses.{expected.__name__}'
        ) as mocked_method:
            if args:
                responses.handle_business_errors(exp_type(args))
            else:
                responses.handle_business_errors(exp_type())

        mocked_method.assert_called_once()


class TestHandleServiceErrors:
    """ Tests for handle_service_errors
    """
    cases = [
        (AuthenticationError, 401, '', responses.unauthorized),
        (AuthorizationError, 403, '', responses.forbidden),
        (InternalServerError, 500, '', responses.internal_server_error),
        (
            InvalidDataError,
            400,
            {
                'code': 'validation_error',
                'reason': {'field': 'error'}
            },
            responses.bad_request
        ),
        (NotFoundError, 404, '', responses.not_found),
        (
            PaymentRequiredError,
            402,
            {'code': 'card_declined', 'reason': 'something bad'},
            responses.payment_required
        ),
        (UnexpectedError, 500, '', responses.internal_server_error),
    ]

    @pytest.mark.parametrize('exp_type,status,body,expected', cases)
    def test_handle_errors(self, exp_type, status, body, expected):
        with patch(
            f'styler_rest_framework.api.responses.{expected.__name__}'
        ) as mocked_method:
            response_text = json.dumps(body)
            responses.handle_service_errors(
                exp_type(status=status, response_text=response_text))

        mocked_method.assert_called_once()
