""" Tests for service error
"""

import json

from styler_rest_framework.exceptions.services import ServiceError


class MockResponse:
    def __init__(self, text):
        self.body_text = text
        self.status = 500

    async def text(self):
        return self.body_text


class TestJsonBody:
    """ Tests for method json_body
    """
    async def test_json_body(self):
        text = json.dumps({'key': 'error'})
        exception = ServiceError(MockResponse(text))

        result = await exception.json_body()

        assert result == {'key': 'error'}

    async def test_non_json_body(self):
        text = 'some text'
        exception = ServiceError(MockResponse(text))

        result = await exception.json_body()

        assert result == {}


class TestText:
    """ Tests for method text
    """
    async def test_text(self):
        text = 'some text'
        exception = ServiceError(MockResponse(text))

        result = await exception.text()

        assert result == 'some text'


class TestStatus:
    """ Tests for method status
    """
    def test_text(self):
        text = 'some text'
        exception = ServiceError(MockResponse(text))

        result = exception.response_status()

        assert result == 500
