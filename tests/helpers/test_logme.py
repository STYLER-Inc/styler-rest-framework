"""Tests for logme
"""
from unittest.mock import patch

from styler_rest_framework.helpers import logme


class TestSendMail:
    """Tests for send_mail
    """
    @patch('styler_rest_framework.pubsub.publishers.publish_message')
    def test_send_mail(self, mocked_message):
        logme.logme(
            'test_dataset',
            'test_table',
            [{"field": "value"}, {"field": "value2"}]
        )

        mocked_message.assert_called_once()