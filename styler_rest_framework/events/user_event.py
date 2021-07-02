from functools import wraps
import json
import time

from styler_rest_framework.api.request_scope import Identity

from styler_rest_framework.pubsub.publishers.messages.save_data_message import (
    SaveDataMessage,
)
from styler_rest_framework.pubsub.publishers import publisher_for_message
from styler_rest_framework.config import defaults


handler = publisher_for_message(SaveDataMessage, defaults.TOPIC_NAME)

_TABLE = f"userEvents-{defaults.ENVIRONMENT}"


def track(func):
    """Track and log all inputs and outputs"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        data = {**extract_args(args), **extract_named_args(kwargs)}
        try:
            result = func(*args, **kwargs)
            data["return"] = json.dumps(result, skipkeys=True)
        finally:
            obj_type = ".".join([func.__module__, func.__name__])
            args_dict = {k: v for k, v in zip(range(len(args)), args)}
            key = "#".join(
                [str(get_user_id({**args_dict, **kwargs})), obj_type, str(time.time())]
            )
            handler(_TABLE, obj_type, key, data)
        return result

    return wrapper


def extract_args(args):
    """Extract the args"""
    inputs = {}
    for arg in args:
        try:
            if "__dict__" in dir(arg):
                value = json.dumps(arg.__dict__)
            elif type(arg) in (int, str, float, bool):
                value = arg
            else:
                value = json.dumps(arg)
        except Exception:
            value = repr(arg)
        inputs[len(inputs.keys())] = value
    return inputs


def extract_named_args(kwargs):
    """Extract the kwargs"""
    inputs = {}
    if not kwargs:
        return inputs
    for k, kwarg in kwargs.items():
        try:
            if "__dict__" in dir(kwarg):
                value = json.dumps(kwarg.__dict__)
            elif type(kwarg) in (int, str, float, bool):
                value = kwarg
            else:
                value = json.dumps(kwarg)
        except Exception:
            value = repr(kwarg)
        inputs[k] = value
    return inputs


def get_user_id(data):
    """Extract the user_id from the identity"""
    if not data:
        return None
    for k, v in data.items():
        if isinstance(v, Identity):
            return v.user_id()
    return None
