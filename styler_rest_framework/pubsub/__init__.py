""" pubsub module
"""

from typing import Any, Callable
import logging

from google.cloud import pubsub_v1


def configure_subscriber(handler: Callable[[Any], None], sub_name: str) -> Any:
    """ Configure a subscriber

        Args:
            handler: message handling callback
            sub_name: Subscription name

        Returns:
            A subscriber listener
    """ subscriber = pubsub_v1.SubscriberClient()
    return subscriber.subscribe(
        sub_name, callback=handler
    )


def start_listening(sub: Any) -> None:
    """ Start listening for messages

        Args:
            sub: Subscriber listener
    """
    logging.info('Start listening...')
    try:
        sub.result()
    except Exception as exc:
        logging.exception('Stopped listening: %s', exc)
        sub.cancel()

