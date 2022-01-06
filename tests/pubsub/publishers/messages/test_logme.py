""" Tests for the LogMe message
"""

import json

from styler_rest_framework.pubsub.publishers.messages.logme_message \
    import (
        LogMeMessage
    )


class TestLogMeMessage:
    """ Tests for SendMail message
    """
    def test_generate_message(self):
        msg = LogMeMessage(
            'test_dataset',
            'test_table',
            [{"field": "value"}, {"field": "value2"}]
        )
        expected_keys_in_message = {
            'dataset',
            'table',
            'rows'
        }

        message_data = msg.encoded()
        decoded = json.loads(str(message_data, encoding='utf-8'))

        assert 'name' in decoded
        assert decoded['name'] == 'LogMe'
        assert 'arg' in decoded
        assert all([k in decoded['arg'] for k in expected_keys_in_message])