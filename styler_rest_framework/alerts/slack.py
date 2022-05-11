from styler_rest_framework.pubsub.publishers.messages.slack_alert_message import (
    FileAlertMessage,
    TextAlertMessage,
)
from styler_rest_framework.pubsub.publishers import publisher_for_message
from styler_rest_framework.config import defaults


send_file_to_slack = publisher_for_message(FileAlertMessage, defaults.SLACK_ALERT_TOPIC)
send_text_to_slack = publisher_for_message(TextAlertMessage, defaults.SLACK_ALERT_TOPIC)
