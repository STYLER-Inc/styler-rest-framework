from styler_rest_framework.pubsub.publishers.messages.logme_message import (
    LogMeMessage,
)
from styler_rest_framework.pubsub.publishers import publisher_for_message
from styler_rest_framework.config import defaults


logme = publisher_for_message(LogMeMessage, defaults.LOGME_TOPIC)
