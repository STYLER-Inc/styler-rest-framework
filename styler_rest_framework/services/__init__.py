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
    ServiceError,
    UnexpectedError,
    ConflictError,
)


class HTTPHandler:
    """Handles HTTP operations"""

    def __init__(self, identity=None, retry_on=None, headers=None):
        if retry_on is None:
            self.retry_on = [503]
        else:
            self.retry_on = retry_on
        self.headers = {}
        if headers is None:
            headers = {}
        if identity:
            self.identity = identity
            self.headers = {
                "Authorization": f"Bearer {identity.token()}",
                **{"Accept-Language": identity.localization()},
                **identity.trace_header()
            }
        self.headers = {
            **self.headers,
            **headers
        }

    async def post(self, url, params, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        try:
            async with ClientSession() as session:
                async with session.post(
                    url, headers=headers, json=params, ssl=True
                ) as resp:
                    if resp.status not in [200, 201]:
                        if error_handlers and resp.status in error_handlers:
                            await error_handlers[resp.status](resp)
                        await self._handle_http_errors(resp)

                    return await resp.json()
        except ServiceError as ex:
            # Retry
            if retry > 0 and ex.status in retry_on:
                return await self.post(
                    url, params, error_handlers=None, retry=retry - 1, **kwargs
                )
            else:
                raise

    async def patch(self, url, params, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))

        try:
            async with ClientSession() as session:
                async with session.patch(
                    url, headers=headers, json=params, ssl=True
                ) as resp:
                    if resp.status not in [200]:
                        if error_handlers and resp.status in error_handlers:
                            await error_handlers[resp.status](resp)
                        await self._handle_http_errors(resp)

                    return await resp.json()
        except ServiceError as ex:
            # Retry
            if retry > 0 and ex.status in retry_on:
                return await self.patch(
                    url, params, error_handlers=None, retry=retry - 1, **kwargs
                )
            else:
                raise

    async def put(self, url, params, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        try:
            async with ClientSession() as session:
                async with session.put(
                    url, headers=headers, json=params, ssl=True
                ) as resp:
                    if resp.status not in [200]:
                        if error_handlers and resp.status in error_handlers:
                            await error_handlers[resp.status](resp)
                        await self._handle_http_errors(resp)

                    return await resp.json()
        except ServiceError as ex:
            # Retry
            if retry > 0 and ex.status in retry_on:
                return await self.put(
                    url, params, error_handlers=None, retry=retry - 1, **kwargs
                )
            else:
                raise

    async def delete(self, url, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        try:
            async with ClientSession() as session:
                async with session.delete(url, headers=headers, ssl=True) as resp:
                    if resp.status not in [200]:
                        if error_handlers and resp.status in error_handlers:
                            await error_handlers[resp.status](resp)
                        await self._handle_http_errors(resp)

                    return await resp.json()
        except ServiceError as ex:
            # Retry
            if retry > 0 and ex.status in retry_on:
                return await self.delete(
                    url, error_handlers=None, retry=retry - 1, **kwargs
                )
            else:
                raise

    async def get(self, url, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        try:
            async with ClientSession() as session:
                async with session.get(url, headers=headers, ssl=True) as resp:
                    if resp.status != 200:
                        if error_handlers and resp.status in error_handlers:
                            await error_handlers[resp.status](resp)
                        await self._handle_http_errors(resp)

                    return await resp.json()
        except ServiceError as ex:
            # Retry
            if retry > 0 and ex.status in retry_on:
                return await self.get(
                    url, error_handlers=None, retry=retry - 1, **kwargs
                )
            else:
                raise

    def _prepare_headers(self, overrides):
        headers = self.headers
        headers.update(overrides)
        return headers

    async def _handle_http_errors(self, resp):
        """Handles HTTP errors"""
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
        elif resp.status == 409:
            raise ConflictError(resp.status, response_text)
        elif resp.status == 500:
            raise InternalServerError(resp.status, response_text)
        else:
            logging.error("Unexpected response code: %s", resp.status)
            raise UnexpectedError(resp.status, response_text)
