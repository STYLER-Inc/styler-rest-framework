""" Defaults used by all modules
"""

import os


SERVICE_NAME = os.getenv('SERVICE_NAME') or 'svc'
CONTAINER_NAME = os.getenv('SERVICE_NAME') or 'container'

ERROR_HANDLER_SERVICE = f'{CONTAINER_NAME}/{SERVICE_NAME}'
