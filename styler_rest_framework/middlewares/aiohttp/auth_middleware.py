""" Middleware to handle exceptions
"""
from typing import List

from aiohttp import web
from styler_rest_framework.helpers.jwt_validator import validate
from styler_rest_framework.config import defaults


def add_auth_middleware(
    app,
    env: str,
    jwks_url: str = None,
    excludes: List[str] = None,
):
    if not jwks_url:  # pragma: no coverage
        jwks_url = defaults.JWKS_URL

    @web.middleware
    async def middleware(request, handler):
        try:
            paths = [] if excludes is None else excludes
            if request.path in paths:
                return await handler(request)
            jwt_token = request.headers.get('AUTHORIZATION')
            if not jwt_token:
                return web.json_response(
                    {'error': 'Missing JWT token'},
                    status=401
                )
            jwt_data = validate(jwt_token.split()[-1], env, jwks_url)
            if not jwt_data:
                return web.json_response(
                    {'error': 'Invalid JWT token'},
                    status=401
                )
            return await handler(request)
        except web.HTTPException:
            raise

    app.middlewares.append(middleware)
    return middleware
