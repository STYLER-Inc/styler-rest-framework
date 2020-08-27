""" Request scope handles the identification of the user and request options
"""

from styler_identity import Identity


class RequestScope(Identity):
    """ Carries information about the request scope
    """
    def __init__(self, request):
        self.request = request
        token = token = get_token_auth_header(request)
        super().__init__(token)

    def localization(self):
        return self.request.headers.get('Accept-Language', 'ja')

    def trace_header(self):
        return self.request.headers.get('trace_header', {})


def get_token_auth_header(request):
    """ Obtains the Access Token from the Authorization Header
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise ValueError('Authorization header is expected')

    parts = auth_header.split()

    if parts[0].lower() != 'bearer':
        raise ValueError('Authorization header must start with Bearer')
    elif len(parts) == 1:
        raise ValueError('Token not found')
    elif len(parts) > 2:
        raise ValueError('Authorization header must be Bearer token')

    token = parts[1]
    return token
