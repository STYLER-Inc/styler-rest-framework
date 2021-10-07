from styler_rest_framework.pubsub.publishers.messages.send_mail_message import (
    SendMailMessage,
)
from styler_rest_framework.pubsub.publishers import publisher_for_message
from styler_rest_framework.config import defaults


send_email = publisher_for_message(SendMailMessage, defaults.MAILER_TOPIC)
