""" Tests for the SaveData message
"""

import json

from styler_rest_framework.pubsub.publishers.messages.save_data_message \
    import (
        SaveDataMessage
    )


class TestSaveDataMessage:
    """ Tests for SaveData message
    """
    def test_generate_message(self):
        msg = SaveDataMessage(
            'my-tbl',
            'module#function',
            'some#key#123456789',
            {'aaa': 123, 'bbb': 333}
        )
        expected_keys_in_message = {
            'table', 'obj_type', 'key', 'data'
        }

        message_data = msg.encoded()
        decoded = json.loads(str(message_data, encoding='utf-8'))

        assert 'name' in decoded
        assert decoded['name'] == 'SaveData'
        assert 'arg' in decoded
        assert all([k in decoded['arg'] for k in expected_keys_in_message])
