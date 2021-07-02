""" Request scope for FastAPI
"""

from typing import Dict, Callable

from jwt.exceptions import InvalidTokenError
import jwt


class Identity:
    """Holds the identity of the logged user"""

    def __init__(self, token):
        self._token = token
        try:
            self._decoded = jwt.decode(self._token, options={"verify_signature": False})
        except InvalidTokenError:
            raise ValueError("Invalid JWT token")

    def user_id(self):
        """Returns the user_id provided by firebase"""
        return self._decoded.get("user_id")

    def is_system_admin(self):
        """Returns a boolean identifying the user as a system administrator"""
        return "sysadmin" in self._roles()

    def is_admin(self):
        """Returns a boolean identifying the user
        as an organization administrator
        """
        return "admin" in self._roles()

    def is_staff(self):
        """Returns a boolean identifying the user
        as a shop staff
        """
        return "staff" in self._roles()

    def shops(self):
        """Returns a list of shop_ids that the user has access to"""
        return self._custom_claims().get("shop", [])

    def organizations(self):
        """Returns a list of organization_ids that the user has access to"""
        return self._custom_claims().get("organization", [])

    def data(self):
        """Return the entire data from the token"""
        return self._decoded

    def token(self):
        """Returns the original JWT token"""
        return self._token

    def _roles(self):
        """Returns the collection of roles"""
        if "roles" not in self._decoded:
            return []
        return self._decoded["roles"]

    def _custom_claims(self):
        """Returns the collection of custom claims"""
        if "claims" not in self._decoded:
            return {}
        return self._decoded["claims"]


class RequestScope(Identity):
    """Carries information about the request scope"""

    def __init__(
        self,
        authorization: str = None,
        accept_language: str = "ja",
        trace: Dict = None,
    ) -> Callable:
        self.accept_language = accept_language
        self.trace = trace or {}
        token = get_token(authorization)
        super().__init__(token)

    def localization(self):
        # Also 'ja' when None is passed.
        return self.accept_language or "ja"

    def trace_header(self):
        return self.trace

    @classmethod
    def from_request(cls, request):
        auth_header = request.headers.get("Authorization")
        accept_language = request.headers.get("Accept-Language", "ja")
        trace = request.headers.get("trace_header", {})
        return cls(
            authorization=auth_header, accept_language=accept_language, trace=trace
        )


def get_token(authorization: str) -> str:
    """Obtains the Access Token from the Authorization Header value"""
    if not authorization:
        raise ValueError("Authorization header is expected")

    parts = authorization.split()

    if parts[0].lower() != "bearer":
        raise ValueError("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise ValueError("Token not found")
    elif len(parts) > 2:
        raise ValueError("Authorization header must be Bearer token")

    token = parts[1]
    return token
