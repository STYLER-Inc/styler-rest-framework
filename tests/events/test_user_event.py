""" Tests for user_event module
"""
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch, Mock
import json

from styler_rest_framework.events import user_event
from styler_rest_framework.api.request_scope import Identity


class TestGetUserId:
    """ Tests for user_event.get_user_id
    """
    def test_get_user_id(self, token):
        data = {
            0: Identity(token(sysadmin=True, user_id='111')),
            1: 'some parameter'
        }

        result = user_event.get_user_id(data)

        assert result == '111'

    def test_no_identity(self, token):
        data = {
            0: '1234',
            1: 'some parameter'
        }

        result = user_event.get_user_id(data)

        assert result is None

    def test_no_data(self, token):
        result = user_event.get_user_id(None)

        assert result is None


class MyCustomClass:
    def __init__(self):
        self.prop1 = '1234'
        self.prop2 = 5555


class TestExtractNamedArgs:
    """ Tests for user_event.extract_named_args
    """
    def test_extract_named_args(self):
        now = datetime.now()
        kwargs = {
            'key1': 'string',
            'key2': 1234,
            'key3': Decimal('12.30'),
            'key4': now,
            'key5': MyCustomClass()
        }

        result = user_event.extract_named_args(kwargs)

        assert result == {
            'key1': 'string',
            'key2': 1234,
            'key3': repr(Decimal('12.30')),
            'key4': repr(now),
            'key5': '{"prop1": "1234", "prop2": 5555}'
        }

    def test_no_data(self):
        result = user_event.extract_named_args(None)

        assert result == {}


class TestExtractArgs:
    """ Tests for user_event.extract_args
    """
    def test_extract_args(self):
        now = datetime.now()
        args = [1, 'something', now, Decimal('20.01'), MyCustomClass()]

        result = user_event.extract_args(args)

        assert result == {
            0: 1,
            1: 'something',
            2: repr(now),
            3: repr(Decimal('20.01')),
            4: '{"prop1": "1234", "prop2": 5555}'
        }


class TestTrack:
    """ Tests for user_event.track
    """
    @patch('styler_rest_framework.events.user_event.handler')
    def test_track_function(self, mocked_handler, token):
        @user_event.track
        def do_something(a, b, c, d):
            return 'something'
        iden = Identity(token(sysadmin=True, user_id='111'))

        with patch(
            'styler_rest_framework.events.user_event.time.time',
            Mock(return_value='timestamp')
        ):
            do_something(1234, 'aaa', c='parameter c', d=iden)

        mocked_handler.assert_called_once_with(
            user_event._TABLE,
            'tests.events.test_user_event.do_something',
            '111#tests.events.test_user_event.do_something#timestamp',
            {
                0: 1234,
                1: 'aaa',
                'c': 'parameter c',
                'd': json.dumps(iden.__dict__),
                'return': '"something"'
            }
        )
