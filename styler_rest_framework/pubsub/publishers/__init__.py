""" Publishing module
"""

from styler_rest_framework.pubsub.publishers.pubsub_handler import publish_message


def publisher_for_message(message_type, topic):
    """Returns a callable to handle publishing a message"""

    def wrapper(*args, **kwargs):
        msg = message_type(*args, **kwargs)
        publish_message(topic, msg.encoded())

    return wrapper
