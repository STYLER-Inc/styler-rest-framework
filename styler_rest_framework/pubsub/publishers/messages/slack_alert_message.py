""" SlackAlert messages
"""

from styler_rest_framework.pubsub.publishers.messages import Message


class FileAlertMessage(Message):
    """FileAlert message"""

    def __init__(self, filename, text, channel=None):
        self.name = "FileAlert"
        self.arg = {}
        self._fill_args(filename, text, channel)

    def _fill_args(self, filename, text, channel):
        """Map fields from FileAlert"""
        self.arg = {"filename": filename, "text": text}
        if channel:
            self.arg["channel"] = channel


class TextAlertMessage(Message):
    """TextAlert message"""

    def __init__(self, text, channel=None):
        self.name = "TextAlert"
        self.arg = {}
        self._fill_args(text, channel)

    def _fill_args(self, text, channel):
        """Map fields from TextAlert"""
        self.arg = {"text": text}
        if channel:
            self.arg["channel"] = channel
