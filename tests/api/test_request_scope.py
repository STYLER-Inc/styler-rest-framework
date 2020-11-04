""" Tests for request_scope module
"""

from unittest.mock import Mock

from styler_rest_framework.api.request_scope import (
    RequestScope,
    get_token,
)
import pytest


class TestGetToken:
    """ Tests for get_token
    """
    def test_get_token(self):
        """ Should return the token
        """
        token = get_token('Bearer TOKEN')

        assert token == 'TOKEN'

    def test_none(self):
        """ Should raise an exception
        """
        with pytest.raises(ValueError) as expected:
            get_token(None)
        assert str(expected.value) == 'Authorization header is expected'

    def test_without_bearer(self):
        """ Should raise an exception if there is no bearer
        """
        with pytest.raises(ValueError) as expected:
            get_token('token TOKEN')
        assert str(expected.value) == \
            'Authorization header must start with Bearer'

    def test_without_token(self):
        """ Should raise an exception if the auth is invalid
        """
        with pytest.raises(ValueError) as expected:
            get_token('Bearer')
        assert str(expected.value) == 'Token not found'

    def test_invalid_auth(self):
        """ Should raise an exception if the Authorization is invalid
        """
        with pytest.raises(ValueError) as expected:
            get_token('Bearer TOKEN TOKEN')
        assert str(expected.value) == \
            'Authorization header must be Bearer token'


@pytest.fixture
def auth():
    return (
        'Bearer '
        'eyJhbGciOiJSUzI1NiIsImtpZCI6Im'
        'MzZjI3NjU0MmJmZmU0NWU5OG'
        'MyMGQ2MDNlYmUyYmExMTc2ZWRhMzMiLCJ0e'
        'XAiOiJKV1QifQ.eyJzeXN0ZW1fYWRta'
        'W4iOmZhbHNlLCJjbGFpbXMiOnsic2hvcHMi'
        'OlsiN2YwNzZjNDgtMGU0Yy00MDQ0LTl'
        'kNDctMjM0MjM0MzI0MjM0IiwiN2YwNzZjND'
        'gtMGU0Yy00MDQ0LTlkNDctMzg4OTk5M'
        'Dk4MDkwIl0sIm9yZ2FuaXphdGlvbnMiOltd'
        'fSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV'
        '0b2tlbi5nb29nbGUuY29tL2ZhY3ktZGV2ZW'
        'xvcG1lbnQiLCJhdWQiOiJmYWN5LWRld'
        'mVsb3BtZW50IiwiYXV0aF90aW1lIjoxNTky'
        'ODg2Mjg5LCJ1c2VyX2lkIjoiNm5hZjg'
        'wanR5YlZSdVAyMmVZY0lZR1gyS0pLMiIsIn'
        'N1YiI6IjZuYWY4MGp0eWJWUnVQMjJlW'
        'WNJWUdYMktKSzIiLCJpYXQiOjE1OTI4ODYy'
        'ODksImV4cCI6MTU5Mjg4OTg4OSwiZW1'
        'haWwiOiJicnVuby5zdWdhbm9Ac3R5bGVyLm'
        'xpbmsiLCJlbWFpbF92ZXJpZmllZCI6Z'
        'mFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRp'
        'ZXMiOnsiZW1haWwiOlsiYnJ1bm8uc3V'
        'nYW5vQHN0eWxlci5saW5rIl19LCJzaWduX2'
        'luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.'
        'VNJtVQ9nmvbpUkMM95cdN06O3NDUqdBwEgm'
        'czfWKR2Vt5fOFQGtFykEovEmajdVHZO'
        'm4tbJlbfoILu0i_GsO-7jaoYNBOC9-tIBiD'
        '8pvUCeL4iQj2jhpvR6z3PEtTyA7i7Ae'
        'VUj9wuxrzYm0wtcLTR1vSEp4jTj3Nw5KD4a'
        'dPq4IF63SKqywNLkmgURuQnF-WlaZBn'
        'g2CK0AMddY0Qt-1Z0IFUp-i_tXkGMOPBjXs'
        'wq1kPxyZ2xtNWZjQZ5sWNw2dmkC2wyf'
        'EmnQ5Zm9UJvrS6tiCigTGkF43PhwTl26K9z'
        'twOtekrpOiwap-c55rUG8TbobpmGGkF'
        'i9Q3r5dHH-ag'
    )


class TestLocalization:
    """ Tests for localization
    """
    def test_localization(self, auth):
        req_scope = RequestScope(
            authorization=auth,
            accept_language='en'
        )

        localization = req_scope.localization()

        assert localization == 'en'

    def test_localization_none(self, auth):
        req_scope = RequestScope(
            authorization=auth
        )

        localization = req_scope.localization()

        assert localization == 'ja'


class TestTraceHeader:
    """ Tests for trace_header
    """
    def test_trace_header(self, auth):
        req_scope = RequestScope(
            authorization=auth,
            trace={'aa': 'bb'}
        )

        trace_header = req_scope.trace_header()

        assert trace_header == {'aa': 'bb'}

    def test_trace_header_none(self, auth):
        req_scope = RequestScope(
            authorization=auth
        )

        trace_header = req_scope.trace_header()

        assert trace_header == {}


class MockHeaders:
    def __init__(self, auth, locale, header=None):
        self.locale = locale
        self.header = header
        self.auth = auth

    def get(self, key, default=None):
        if key == 'Authorization':
            return self.auth
        if key == 'Accept-Language':
            return self.locale or default
        if key == 'trace_header':
            return self.header or {}


class TestFromRequest:
    """ Tests for class method from_request
    """
    def test_from_request(self, auth):
        request = Mock()
        request.headers = MockHeaders(
            auth=auth, locale='en', header={'aa': '1234'})

        req_scope = RequestScope.from_request(request)

        assert req_scope.localization() == 'en'
        assert req_scope.trace_header() == {'aa': '1234'}
