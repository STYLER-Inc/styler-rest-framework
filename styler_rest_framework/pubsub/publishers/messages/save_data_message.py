""" SaveData message
"""

from styler_rest_framework.pubsub.publishers.messages import Message


class SaveDataMessage(Message):
    """Generate SaveData message body"""

    def __init__(self, table, obj_type, key, data):
        self.name = "SaveData"
        self.arg = {"table": table, "obj_type": obj_type, "key": key, "data": data}
