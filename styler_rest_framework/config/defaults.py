""" Defaults used by all modules
"""

import os


SERVICE_NAME = os.getenv('SERVICE_NAME') or 'svc'
NAMESPACE = os.getenv('NAMESPACE') or 'namespace'
VERSION = os.getenv('VERSION') or '0.1.0'

ERROR_HANDLER_SERVICE = f'{NAMESPACE}/{SERVICE_NAME}'

ENVIRONMENT = os.getenv('ENVIRONMENT')
TOPIC_NAME = os.getenv('TOPIC_NAME') or \
    f'projects/facy-{ENVIRONMENT}/topics/common'
