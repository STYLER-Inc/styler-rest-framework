""" Request scope for FastAPI
"""

from typing import Dict, Callable

from styler_identity import Identity


class RequestScope(Identity):
    """ Carries information about the request scope
    """
    def __init__(
        self,
        authorization: str = None,
        accept_language: str = 'ja',
        trace: Dict = None,
    ) -> Callable:
        self.accept_language = accept_language
        self.trace = trace or {}
        token = get_token(authorization)
        super().__init__(token)

    def localization(self):
        # Also 'ja' when None is passed.
        return self.accept_language or 'ja'

    def trace_header(self):
        return self.trace

    @classmethod
    def from_request(cls, request):
        auth_header = request.headers.get('Authorization')
        accept_language = request.headers.get('Accept-Language', 'ja')
        trace = request.headers.get('trace_header', {})
        return cls(
            authorization=auth_header,
            accept_language=accept_language,
            trace=trace
        )


def get_token(authorization: str) -> str:
    """ Obtains the Access Token from the Authorization Header value
    """
    if not authorization:
        raise ValueError('Authorization header is expected')

    parts = authorization.split()

    if parts[0].lower() != 'bearer':
        raise ValueError('Authorization header must start with Bearer')
    elif len(parts) == 1:
        raise ValueError('Token not found')
    elif len(parts) > 2:
        raise ValueError('Authorization header must be Bearer token')

    token = parts[1]
    return token
