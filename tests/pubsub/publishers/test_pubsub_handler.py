""" Tests for the shops publisher
"""

from unittest.mock import Mock, patch

from styler_rest_framework.pubsub.publishers import (
    pubsub_handler as handler,
    publisher_for_message,
)
from styler_rest_framework.pubsub.publishers.messages import (
    Message
)
import pytest


class TestGetCallback:
    """ Tests for get_callback
    """
    def test_callback(self):
        """ Should return a callable
        """
        data = Mock()

        result = handler.get_callback(data)

        assert callable(result)

    @patch('logging.error')
    def test_callback_raise(self, mocked_logging):
        """ The callable should raise an error
        """
        data = Mock()
        result = handler.get_callback(data)

        with pytest.raises(Exception) as expected:
            api_future = Mock()
            api_future.result.side_effect = Exception('Something went wrong')
            result(api_future)

        assert str(expected.value) == 'Something went wrong'
        mocked_logging.assert_called_once()


class MockMessage(Message):
    def __init__(self, some_data):
        self.name = 'MockMessage'
        self.arg = some_data


class TestPublisher:
    """Tests for publisher
    """
    @patch('styler_rest_framework.pubsub.publishers.publish_message')
    def test_publisher_for_message(self, mocked_publisher):
        func = publisher_for_message(MockMessage, 'my-topic')

        func({'aaa': 123})

        mocked_publisher.assert_called_once()
