
from functools import wraps
import asyncio

from fastapi.responses import JSONResponse
from styler_rest_framework.api.request_scope import RequestScope


class Role:
    SYSADMIN = 4
    ADMIN = 2
    STAFF = 1


def highest_role(roles):
    if 'sysadmin' in roles:
        return Role.SYSADMIN
    elif 'admin' in roles:
        return Role.ADMIN
    elif 'staff' in roles:
        return Role.STAFF
    else:
        return 0


def authorize(role: int):
    """Verifies if the JWT contains at least the minimum required role.

    :param role: Minimum required role
    :type role: int
    """
    def has_roles(func):
        @wraps(func)
        async def awrapper(*args, **kwargs):
            token = kwargs.get('authorization')
            if not token:
                return JSONResponse(status_code=403)
            identity = RequestScope(authorization=token)
            if highest_role(identity._roles()) < role:
                return JSONResponse(status_code=403)
            return await func(*args, **kwargs)

        @wraps(func)
        def wrapper(*args, **kwargs):
            token = kwargs.get('authorization')
            if not token:
                return JSONResponse(status_code=403)
            identity = RequestScope(authorization=token)
            if highest_role(identity._roles()) < role:
                return JSONResponse(status_code=403)
            return func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return awrapper
        else:
            return wrapper

    return has_roles
