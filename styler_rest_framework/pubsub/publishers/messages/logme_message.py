""" Message template for logme
"""

from styler_rest_framework.pubsub.publishers.messages import Message
from styler_rest_framework.config import defaults

class LogMeMessage(Message):
    """ Generates LogMe message body. """

    def __init__(self, dataset, table, rows):
        self.name = "LogMe"
        self.arg = {}
        self._fill_args(dataset, table, rows)

    def _fill_args(self, dataset, table, rows):
        """ Map fields """
        self.arg = {
            "dataset": dataset,
            "table": table,
            "rows": rows
        }