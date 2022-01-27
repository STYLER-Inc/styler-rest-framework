""" Defaults used by all modules
"""

import os


SERVICE_NAME = os.getenv("SERVICE_NAME") or "svc"
CONTAINER_NAME = os.getenv("CONTAINER_NAME") or "api"
NAMESPACE = os.getenv("NAMESPACE") or "namespace"
VERSION = os.getenv("VERSION") or "0.1.0"

ERROR_HANDLER_SERVICE = f"{NAMESPACE}/{CONTAINER_NAME}"

ENVIRONMENT = os.getenv("ENVIRONMENT")
TOPIC_NAME = os.getenv("TOPIC_NAME") or f"projects/facy-{ENVIRONMENT}/topics/common"
MAILER_TOPIC = os.getenv("MAILER_TOPIC") or f"projects/facy-{ENVIRONMENT}/topics/send-email"
LOGME_TOPIC = os.getenv("LOGME_TOPIC") or f"projects/facy-{ENVIRONMENT}/topics/logme"

# Mailer
EMAIL_SENDER = os.getenv("EMAIL_SENDER") or "info@styler.link"
EMAIL_SENDER_NAME = os.getenv("EMAIL_SENDER_NAME") or "FACYカスタマーサポート"
EMAIL_TYPE = os.getenv("EMAIL_TYPE") or "text/html"

# JWKS
JWKS_URL = os.getenv("JWKS_URL") or "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
