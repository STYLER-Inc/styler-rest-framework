""" Handles creation of messages
"""

import json


class Message:
    """Base message"""

    def encoded(self):
        """Return a encoded data for pub sub"""
        json_string = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return json_string.encode("utf-8")
