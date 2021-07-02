""" Messages templates
"""

from styler_rest_framework.pubsub.publishers.messages import Message
from styler_rest_framework.config import defaults


class SendMailMessage(Message):
    """Generate SendMail message body"""

    def __init__(
        self,
        receiver,
        title,
        body,
        cc=None,
        sender_email=None,
        sender_name=None,
        email_type=None,
    ):
        self.name = "SendMail"
        self.arg = {}
        self._fill_args(
            sender_email, receiver, title, body, cc, sender_name, email_type
        )

    def _fill_args(
        self, sender_email, receiver, title, body, cc, sender_name, email_type
    ):
        """Map fields from email"""
        self.arg = {
            "sender": [
                sender_email or defaults.EMAIL_SENDER,
                sender_name or defaults.EMAIL_SENDER_NAME,
            ],
            "receiver": [receiver],
            "cc": cc or [],
            "title": title,
            "body": body,
            "type": email_type or defaults.EMAIL_TYPE,
        }
