""" Tests for the SendMail message
"""

import json

from styler_rest_framework.pubsub.publishers.messages.send_mail_message \
    import (
        SendMailMessage
    )


class TestSendMailMessage:
    """ Tests for SendMail message
    """
    def test_generate_message(self):
        msg = SendMailMessage(
            'mail@mail.com',
            'Some title',
            'Body here'
        )
        expected_keys_in_message = {
            'sender',
            'receiver',
            'cc',
            'title',
            'body',
            'type',
        }

        message_data = msg.encoded()
        decoded = json.loads(str(message_data, encoding='utf-8'))

        assert 'name' in decoded
        assert decoded['name'] == 'SendMail'
        assert 'arg' in decoded
        assert all([k in decoded['arg'] for k in expected_keys_in_message])
