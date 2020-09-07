""" Message handling module
"""

from json.decoder import JSONDecodeError
from typing import Any, Callable, Dict
import json
import logging


class MessageRouter:
    """ Handles and routes messages to mapping handlers
    """

    def __init__(self):
        self._routes = {}

    def handle_message(self, message: Any) -> None:
        """ Route the incoming messages

            Args:
                message: message received from pull
        """
        logging.info('Received message: %s', message)

        message.ack()

        valid, body = self._validate_envelope(message.data)
        if not valid:
            logging.error('Message is not valid: %s', message.data)
            return

        message_name = body['name']
        if message_name in self._routes:
            self._routes[message_name](body['arg'])
        else:
            logging.info('Unknown message name: %s', message_name)

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
                A tuple containing a boolean that indicates
                whether the envelope is valid or not, and a
                object resulted from parsing the argument.
                If the envelope is invalid, (False, None)
                is returned.
        """
        try:
            body = json.loads(data)
        except JSONDecodeError:
            logging.exception('Invalid data')
            return (False, None)

        if 'name' not in body or 'arg' not in body:
            logging.error('Missing parameters in message.data')
            return (False, None)
        return (True, body)
