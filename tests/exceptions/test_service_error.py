""" Tests for service error
"""

import json

from styler_rest_framework.exceptions.services import ServiceError


class TestJsonBody:
    """ Tests for method json_body
    """
    def test_json_body(self):
        text = json.dumps({'key': 'error'})
        exception = ServiceError(status=400, response_text=text)

        result = exception.json_body()

        assert result == {'key': 'error'}

    def test_non_json_body(self):
        text = 'some text'
        exception = ServiceError(status=400, response_text=text)

        result = exception.json_body()

        assert result == {}
