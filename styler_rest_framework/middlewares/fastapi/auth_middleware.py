""" Middleware to handle exceptions
"""
from typing import List
import logging
import re

try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import JSONResponse
except Exception:
    logging.exception(f'Missing libraries: pipenv install fastapi')

from styler_rest_framework.helpers.jwt_validator import validate
from styler_rest_framework.config import defaults


def add_auth_middleware(
    app: FastAPI,
    env: str,
    jwks_url: str = None,
    excludes: List[str] = None,
    excludes_regex: List[str] = None,
):
    if not jwks_url:  # pragma: no coverage
        jwks_url = defaults.JWKS_URL

    @app.middleware("http")
    async def validate_jwt(request: Request, call_next):
        try:
            paths = [] if excludes is None else excludes
            regex_paths = [] if excludes_regex is None else excludes_regex
            if request.url.path in paths:
                return await call_next(request)
            for regex_path in regex_paths:
                if re.match(regex_path, request.url.path):
                    return await call_next(request)
            jwt_token = request.headers.get('Authorization')
            if not jwt_token:
                return JSONResponse(status_code=401, content={'error': 'Missing JWT token'})
            jwt_data = validate(jwt_token.split()[-1], env, jwks_url)
            if not jwt_data:
                return JSONResponse(status_code=401, content={'error': 'Invalid JWT token'})

            return await call_next(request)
        except HTTPException:  # pragma: no coverage
            raise
