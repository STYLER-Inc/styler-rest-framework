""" Handler for pubsub
"""
from concurrent import futures
import logging

from google.cloud import pubsub_v1


def get_callback(data):
    """Wrap message data in the context of the callback function."""

    def callback(api_future):
        try:
            api_future.result()
        except Exception:
            logging.error(
                "A problem occurred when publishing %s: %s\n",
                data,
                api_future.exception(),
            )
            raise

    return callback


def publish_message(topic_name, data):  # pragma: no coverage
    """Publishes a message to a Pub/Sub topic."""
    # Initialize a Publisher client.
    client = pubsub_v1.PublisherClient()
    metadata = {"version": "1"}

    # When you publish a message, the client returns a future.
    api_future = client.publish(topic_name, data=data, **metadata)
    api_future.add_done_callback(get_callback(data))

    futures.wait([api_future], return_when=futures.ALL_COMPLETED)
