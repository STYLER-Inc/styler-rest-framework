""" Middleware to handle exceptions
"""
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


def add_exception_middleware(
    app: FastAPI,
    generic_message="An error has occurred",
    status_code=500,
    error_handler=None,
):
    """Generate a middleware that logs unexpected exceptions
    and returns a JSON response.
    Exceptions of type HTTPException won't be handled as they should be
    expected exceptions.

    Args:
        app: FastAPI application
        generic_message: The message that will be send as an error
        status_code: The HTTP status code (default = 500)
        error_handler: Callable(request, exception)
    """

    @app.middleware("http")
    async def handle_exception(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException:
            raise
        except Exception as ex:
            message = str(ex)
            if error_handler:
                error_handler(request, ex)
            logging.exception("Error: %s", message)
            return JSONResponse(
                status_code=status_code,
                content={"error": generic_message},
            )
