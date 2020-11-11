""" Defaults used by all modules
"""

import os


SERVICE_NAME = os.getenv('SERVICE_NAME') or 'svc'
NAMESPACE = os.getenv('NAMESPACE') or 'namespace'

ERROR_HANDLER_SERVICE = f'{NAMESPACE}/{SERVICE_NAME}'
