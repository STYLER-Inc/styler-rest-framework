""" Middleware to handle exceptions
"""
import logging

try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import JSONResponse
except Exception:
    logging.exception(f'Missing libraries: pipenv install fastapi')

from styler_rest_framework.middlewares.fastapi.jwt_validator import validate
from styler_rest_framework.config import defaults


def add_auth_middleware(
    app: FastAPI,
    env: str,
    jwks_url: str = None
):
    if not jwks_url:
        jwks_url = defaults.JWKS_URL

    @app.middleware("http")
    async def validate_jwt(request: Request, call_next):
        try:
            jwt_token = request.headers.get('Authorization')
            if not jwt_token:
                return JSONResponse(status_code=401, content={'error': 'Missing JWT token'})
            jwt_data = validate(jwt_token.split()[1], env, jwks_url)
            if not jwt_data:
                return JSONResponse(status_code=401, content={'error': 'Invalid JWT token'})

            response = await call_next(request)
            return response
        except HTTPException:
            raise
