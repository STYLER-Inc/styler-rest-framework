"""Tests for mailer
"""
from unittest.mock import patch

from styler_rest_framework.helpers import mailer


class TestSendMail:
    """Tests for send_mail
    """
    @patch('styler_rest_framework.pubsub.publishers.publish_message')
    def test_send_mail(self, mocked_message):
        mailer.send_email('some@mail.com', 'Some title', 'a body')

        mocked_message.assert_called_once()
