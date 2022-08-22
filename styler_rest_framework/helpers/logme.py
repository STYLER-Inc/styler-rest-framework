import logging

from styler_rest_framework.pubsub.publishers.messages.logme_message import (
    LogMeMessage,
)
from styler_rest_framework.pubsub.publishers import publisher_for_message
from styler_rest_framework.config import defaults


if defaults.ENVIRONMENT in ('staging', 'production'):
    logme = publisher_for_message(LogMeMessage, defaults.LOGME_TOPIC)
else:
    def logme(*args, **kwargs):
        logging.info(f'Logme called with args: {args}, kwargs: {kwargs}')
