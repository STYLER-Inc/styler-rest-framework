""" Tests for the shops publisher
"""

import json
from unittest.mock import Mock

from styler_rest_framework.pubsub import MessageRouter


class TestAddRoute:
    """ Tests for add_route
    """
    def test_add_route(self):
        router = MessageRouter()

        router.add_route('my_msg', Mock())

        assert 'my_msg' in router._routes


class TestHandleMessage:
    """ Tests for handle_message
    """
    def test_ack_message(self):
        message = Mock()
        router = MessageRouter()

        router.handle_message(message)

        message.ack.assert_called_once()

    def test_handle_errors_invalid_body(self):
        message = Mock()
        error_handler = Mock()
        router = MessageRouter(error_handler=error_handler)

        router.handle_message(message)

        error_handler.assert_called_once()

    def test_handle_errors_missing_parameters(self):
        message = Mock()
        message.data = json.dumps({'aaa': 'bbb'})
        error_handler = Mock()
        router = MessageRouter(error_handler=error_handler)

        router.handle_message(message)

        error_handler.assert_called_once()

    def test_handle_no_errors(self):
        message = Mock()
        message.data = json.dumps({'name': 'my_msg', 'arg': {'aaa': 'bbb'}})
        error_handler = Mock()
        router = MessageRouter(error_handler=error_handler)
        msg_handler = Mock()
        router.add_route('my_msg', msg_handler)

        router.handle_message(message)

        error_handler.assert_not_called()
        msg_handler.assert_called_once()

    def test_handle_no_route(self):
        message = Mock()
        message.data = json.dumps({'name': 'my_msg', 'arg': {'aaa': 'bbb'}})
        error_handler = Mock()
        router = MessageRouter(error_handler=error_handler)
        msg_handler = Mock()
        router.add_route('other', msg_handler)

        router.handle_message(message)

        error_handler.assert_not_called()
        msg_handler.assert_not_called()
