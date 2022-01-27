from datetime import datetime
from time import time
import logging

try:
    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.backends import default_backend
    from jwt.exceptions import InvalidTokenError
    import jwt
    import requests
except Exception:
    logging.error('Missing libraries:  try  pipenv install "pyjwt[crypto]"')


CURRENT_JWKS = None
EXPIRATION = None


def retrieve_kid(token):  # pragma: no coverage
    return jwt.get_unverified_header(token)['kid']


def public_key(x509):  # pragma: no coverage
    cert_obj = load_pem_x509_certificate(str.encode(x509), default_backend())
    return cert_obj.public_key();


def google_x509(url):  # pragma: no coverage
    response = requests.get(url)
    return response.json(), datetime.strptime(response.headers['Expires'], '%a, %d %b %Y %H:%M:%S GMT')


def verify_token(tk_json):  # pragma: no coverage
    if tk_json['exp'] < time():
        raise ValueError('Expired')
    if tk_json['iat'] > time():
        raise ValueError('Invalid issued at time')
    if tk_json['auth_time'] > time():
        raise ValueError('Invalid authentication time')

def validate(token, env, jwks_url):  # pragma: no coverage
    global CURRENT_JWKS
    global EXPIRATION

    # Verify if the keys have expired
    if not EXPIRATION or EXPIRATION < datetime.utcnow():
        # Refresh JWKS
        CURRENT_JWKS, EXPIRATION = google_x509(jwks_url)
    try:
        # Retrieve the kid from the token
        kid = retrieve_kid(token)

        # Retrieve the public key from the x509 certificate
        pub = public_key(CURRENT_JWKS[kid])

        # Validate JWT using the public key

        data = jwt.decode(
            token,
            pub,
            algorithms=["RS256"],
            audience=f'facy-{env}',
            issuer=f'https://securetoken.google.com/facy-{env}',
            options={'verify_exp': True}
        )
        verify_token(data)
        return data
    except InvalidTokenError as ex:
        logging.exception(ex)
        return None
