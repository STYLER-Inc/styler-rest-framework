""" Message handling module
"""

from typing import Any, Callable, Dict
import json
import logging

from styler_rest_framework.logging import error_reporting
from styler_rest_framework.config import defaults


class MessageRouter:
    """ Handles and routes messages to mapping handlers
    """

    def __init__(self, error_handler=None):
        self._routes = {}
        self.error_handler = error_handler or \
            error_reporting.google_error_reporting_handler(
                service=defaults.ERROR_HANDLER_SERVICE)

    def handle_message(self, message: Any) -> None:
        """ Route the incoming messages

            Args:
                message: message received from pull
        """
        logging.info('Received message: %s', message)

        message.ack()

        try:
            body = self._validate_envelope(message.data)

            message_name = body['name']
            if message_name in self._routes:
                self._routes[message_name](body['arg'])
            else:
                logging.info('Unknown message name: %s', message_name)
        except Exception:
            if self.error_handler:
                self.error_handler()
            logging.exception('Error when handling the message')

    def add_route(self,
                  message_name: str,
                  message_handler: Callable[[Any, Any], None]) -> None:
        """ Register a message route

            Args:
                message_name: expected message name.
                message_handler: function that receives a database connection
                    and the args received in the message.
        """
        self._routes[message_name] = message_handler

    def _validate_envelope(self, data: str) -> (bool, Dict):
        """ Validates the envelope of the data

            Args:
                data: the data received from the message
            Returns:
                The JSON parsed body data
        """
        body = json.loads(data)
        if 'name' not in body or 'arg' not in body:
            raise KeyError('Missing name or arg in the message body')
        return body
