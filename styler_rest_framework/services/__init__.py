""" Services module
"""

import logging

from aiohttp import ClientSession
from styler_rest_framework.exceptions.services import (
    AuthenticationError,
    AuthorizationError,
    InternalServerError,
    InvalidDataError,
    NotFoundError,
    PaymentRequiredError,
    UnexpectedError,
)


class HTTPHandler:
    """ Handles HTTP operations
    """
    def __init__(self, identity, headers=None):
        self.identity = identity
        if headers is None:
            headers = {}
        self.headers = {
            'Authorization': f'Bearer {identity.token()}',
            **{'Accept-Language': identity.localization()},
            **identity.trace_header(),
            **headers
        }

    async def post(self, url, params, error_handlers=None, **kwargs):
        headers = self._prepare_headers(kwargs.get('headers', {}))
        async with ClientSession() as session:
            async with session.post(url,
                                    headers=headers,
                                    json=params,
                                    ssl=True) as resp:
                if resp.status not in [200, 201]:
                    if error_handlers and resp.status in error_handlers:
                        await error_handlers[resp.status](resp)
                    await self._handle_http_errors(resp)

                return await resp.json()

    async def patch(self, url, params, error_handlers=None, **kwargs):
        headers = self._prepare_headers(kwargs.get('headers', {}))
        async with ClientSession() as session:
            async with session.patch(url,
                                     headers=headers,
                                     json=params,
                                     ssl=True) as resp:
                if resp.status not in [200]:
                    if error_handlers and resp.status in error_handlers:
                        await error_handlers[resp.status](resp)
                    await self._handle_http_errors(resp)

                return await resp.json()

    async def put(self, url, params, error_handlers=None, **kwargs):
        headers = self._prepare_headers(kwargs.get('headers', {}))
        async with ClientSession() as session:
            async with session.put(url,
                                   headers=headers,
                                   json=params,
                                   ssl=True) as resp:
                if resp.status not in [200]:
                    if error_handlers and resp.status in error_handlers:
                        await error_handlers[resp.status](resp)
                    await self._handle_http_errors(resp)

                return await resp.json()

    async def delete(self, url, error_handlers=None, **kwargs):
        headers = self._prepare_headers(kwargs.get('headers', {}))
        async with ClientSession() as session:
            async with session.delete(url, headers=headers, ssl=True) as resp:
                if resp.status not in [200]:
                    if error_handlers and resp.status in error_handlers:
                        await error_handlers[resp.status](resp)
                    await self._handle_http_errors(resp)

                return await resp.json()

    async def get(self, url, error_handlers=None, **kwargs):
        headers = self._prepare_headers(kwargs.get('headers', {}))
        async with ClientSession() as session:
            async with session.get(url, headers=headers, ssl=True) as resp:
                if resp.status != 200:
                    if error_handlers and resp.status in error_handlers:
                        await error_handlers[resp.status](resp)
                    await self._handle_http_errors(resp)

                return await resp.json()

    def _prepare_headers(self, overrides):
        headers = self.headers
        headers.update(overrides)
        return headers

    async def _handle_http_errors(self, resp):
        """ Handles HTTP errors
        """
        response_text = await resp.text()
        if resp.status == 400:
            raise InvalidDataError(resp.status, response_text)
        elif resp.status == 401:
            raise AuthenticationError(resp.status, response_text)
        elif resp.status == 402:
            raise PaymentRequiredError(resp.status, response_text)
        elif resp.status == 403:
            raise AuthorizationError(resp.status, response_text)
        elif resp.status == 404:
            raise NotFoundError(resp.status, response_text)
        elif resp.status == 500:
            raise InternalServerError(resp.status, response_text)
        else:
            logging.error('Unexpected response code: %s', resp.status)
            raise UnexpectedError(resp.status, response_text)
