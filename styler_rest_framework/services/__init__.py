""" Services module
"""

from time import time
import json
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
from styler_rest_framework.helpers.logme import logme
from styler_rest_framework.config import defaults


class HTTPHandler:
    """Handles HTTP operations"""

    def __init__(self, identity=None, retry_on=None, headers=None, log=None):
        if retry_on is None:
            self.retry_on = [503]
        else:
            self.retry_on = retry_on
        self.headers = {}
        if headers is None:
            headers = {}
        self.identity = None
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
        self.log_requests = log if log is not None else defaults.INTERNAL_REQUESTS_LOG_ALL

    async def post(self, url, params, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        log_params = [
            defaults.SERVICE_NAME,
            url,
            "POST",
            headers.get("Authorization"),
            json.dumps(params),
            json.dumps(self.identity.trace_header()) if self.identity else ""
        ]

        try:
            async with ClientSession() as session:
                async with session.post(
                    url, headers=headers, json=params, ssl=True
                ) as resp:
                    log_params.extend([resp.status, await resp.text()])
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
        finally:
            if self.log_requests:
                self.log_request(
                    *log_params
                )

    async def patch(self, url, params, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        log_params = [
            defaults.SERVICE_NAME,
            url,
            "PATCH",
            headers.get("Authorization"),
            json.dumps(params),
            json.dumps(self.identity.trace_header()) if self.identity else ""
        ]

        try:
            async with ClientSession() as session:
                async with session.patch(
                    url, headers=headers, json=params, ssl=True
                ) as resp:
                    log_params.extend([resp.status, await resp.text()])
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
        finally:
            if self.log_requests:
                self.log_request(
                    *log_params
                )

    async def put(self, url, params, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        log_params = [
            defaults.SERVICE_NAME,
            url,
            "PUT",
            headers.get("Authorization"),
            json.dumps(params),
            json.dumps(self.identity.trace_header()) if self.identity else ""
        ]

        try:
            async with ClientSession() as session:
                async with session.put(
                    url, headers=headers, json=params, ssl=True
                ) as resp:
                    log_params.extend([resp.status, await resp.text()])
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
        finally:
            if self.log_requests:
                self.log_request(
                    *log_params
                )

    async def delete(self, url, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        log_params = [
            defaults.SERVICE_NAME,
            url,
            "DELETE",
            headers.get("Authorization"),
            "",
            json.dumps(self.identity.trace_header()) if self.identity else ""
        ]

        try:
            async with ClientSession() as session:
                async with session.delete(url, headers=headers, ssl=True) as resp:
                    log_params.extend([resp.status, await resp.text()])
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
        finally:
            if self.log_requests:
                self.log_request(
                    *log_params
                )

    async def get(self, url, error_handlers=None, retry=3, **kwargs):
        retry_on = kwargs.get("retry_on") or self.retry_on
        headers = self._prepare_headers(kwargs.get("headers", {}))
        log_params = [
            defaults.SERVICE_NAME,
            url,
            "GET",
            headers.get("Authorization"),
            "",
            json.dumps(self.identity.trace_header()) if self.identity else ""
        ]

        try:
            async with ClientSession() as session:
                async with session.get(url, headers=headers, ssl=True) as resp:
                    log_params.extend([resp.status, await resp.text()])
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
        finally:
            if self.log_requests:
                self.log_request(
                    *log_params
                )

    def log_request(
            self,
            origin_service: str = None,
            path: str = None,
            method: str = None,
            auth: str = None,
            request_body: str = None,
            request_tags: str = None,
            response_status_code: int = None,
            response_body: str = None):  # pragma: no coverage
        """Logs the request/response

        :param origin_service: Service sender, defaults to None
        :type origin_service: str, optional
        :param path: URL, defaults to None
        :type path: str, optional
        :param method: HTTP Method, defaults to None
        :type method: str, optional
        :param auth: Auth JWT, defaults to None
        :type auth: str, optional
        :param request_body: JSON string, defaults to None
        :type request_body: str, optional
        :param request_tags: Identifiers, defaults to None
        :type request_tags: str, optional
        :param response_status_code: HTTP Response status code, defaults to None
        :type response_status_code: int, optional
        :param response_body: JSON string, defaults to None
        :type response_body: str, optional
        """
        try:
            logme(
                defaults.INTERNAL_REQUESTS_DATASET,
                defaults.INTERNAL_REQUESTS_TABLE,
                [
                    (origin_service, path, method, auth, request_body, int(time()), request_tags, response_status_code, response_body)
                ]
            )
        except Exception as ex:
            logging.warning(f"Could not log request: {str(ex)}")

    def get_trace_header(self, headers=None):
        headers = headers or self.headers


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
