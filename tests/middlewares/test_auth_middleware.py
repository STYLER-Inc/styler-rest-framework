""" Tests for the exception middleware
"""
from unittest.mock import Mock, patch, AsyncMock

from styler_rest_framework.middlewares.fastapi import auth_middleware
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pytest


class MockFastAPI:
    def __init__(self):
        self.middleware_func = None

    def middleware(self, middleware_type):
        def decorator(func):
            self.middleware_func = func
        return decorator


class TestAddAuthMiddleware:
    """ Tests for add_auth_middleware
    """
    def test_add_auth_middleware(self):
        app = MockFastAPI()

        auth_middleware.add_auth_middleware(app, 'development')

        assert app.middleware_func is not None
        assert callable(app.middleware_func)


class TestValidateJWTException:
    """ Tests for validating JWT
    """
    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=True))
    async def test_valid_jwt(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development')
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjNhYTE0OGNkMDcyOGUzMDNkMzI2ZGU1NjBhMzVmYjFiYTMyYTUxNDkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoib3JnYW5pemF0aW9uIGFkbWluIChzdGcpIiwicm9sZXMiOlsiYWRtaW4iLCJzdGFmZiJdLCJjbGFpbXMiOnsib3JnYW5pemF0aW9uIjpbIjQxM2QzZjMwLTQxODUtNDJmZi05Mzc5LTIxZTdhNWQ1OWViNiIsIjhjZmI5YmJiLTgzODEtNGRjNC05ZmRhLTVmOTEyMTliYTM0YiJdLCJzaG9wIjpbImIxZDRlMzk2LWY4ZGEtNDU5Ni04MGE3LTJhNjdmZmI5MjIxZCIsImFhNDhmZjAyLTU3OGItNGQ2ZS05ZGM2LWNiM2FkYTc3NDg4NCIsImMzMWE2OWRlLWRhMDktNDUyNi05ZTkzLWE3ZjY5MDM3NWRhOCIsIjBlYWM0NTllLWZkZmEtNDRkNS1hZTViLWQ1YWVlNjRkNGY4MiIsImFlODAxMGIxLWM2MTYtNDdjYy1hNTE0LWQxOWZhM2E4NGQ1MiIsIjZmMWExN2JlLTFmODItNDVlNi04MDg5LWYzOTc4MWY4YWI0MSIsIjBiMWZhM2FjLTQ2OGQtNGM4ZS04YjhmLTQzY2Q1NjlkYjAxNSIsIjQ3ZmQ5MDYwLTc2ZDctNDQ4OC1iNTcyLTUxNTkyODNlOTEzYiIsImU3YzQyNzY1LTI5NWMtNDE5Yi04MTdjLWVlNzk5Y2U0MWYwYiIsIjY4YTVhYTM2LTA5NTYtNDJmNy1hOGEzLTkwZjJiYjg0ZWM1NCIsIjNhMmY1ZDAxLTJlYjItNDkyOS04Y2NjLWQwNTY0YWZkOWFjNiIsImRiMTQ3MmEyLTcwOGUtNDQ5Mi1hNzhiLTJhMDFjM2EwZjQ4ZCIsImZhZjNlMTJkLWY4NzMtNDhhZi1iNjNjLTM0ZmJhODJmMWFkOSIsImRlZDFjNDAyLTI4MGUtNDc4ZS1hMDY2LWNlNjk4YWEwYTIyZCIsIjdjZTAwZTRjLWU5M2QtNGE5Mi04ZTlkLTI1MDM0MWM2YWNlYSIsIjliMWY5MzhiLTVlMmMtNDVkYS1hNTc4LWZhNGZjNDUyZDhlZSIsIjBiNTVjMWQ4LThhZGQtNDljMy1iMTM5LTNhZmI1YWY5YTg1ZCIsIjRmYzA4ODY1LWUyNzUtNDFkOS05NzdiLTY1ZjE2ZjJiYTVkYSIsIjg5MTY0OTk1LTIyNzQtNDNlNC1hYTU1LTc1MWM3YmZjYmYzZCIsImU2YmYxNWNjLTJmZTUtNGUwYi04OWExLTY3NzNkNzZmMzc5YSIsIjMyNjM4ZDRhLTU3NGQtNDNlYS1hNGI5LTMzODIwYjIwYjFiZCIsImIxZmY2NTVmLTZjY2UtNGNiMC1hNWM2LTcwOWYzNmI5YjIxNCIsIjM3ZThmZGM1LTkwZDYtNDkxYi1iNzQ1LTIwZGRiNzAwZjUxMSIsIjY5ZjFiOWNhLTk2OTAtNDliOC1iMTAzLWUxYzYxNTUwMDhkMSIsIjJhZmE2NDkyLTc1MDItNGE0YS04MWE1LTc3NjgzNTZkODFiYiIsIjdjOTlmMWIyLTU3YWUtNDE1NS1iNzZkLWViZGNiMWNkNjc1OSIsImYxNWU2YTMyLTM0YmEtNGNkYi05NDFmLTJhYTE1ZDMyZjdlYSIsIjg1YTRkOTc1LTczZjgtNDNmYi05OTRlLWE0NjI4NDZlZDE4OCIsImI2OTIxNjM2LWYyNzctNDc2My04YmI4LWE0MjdlN2EwZDVkNiIsIjlhNGY2YWU5LTM2NWMtNDJhNy04MTJlLTEyYjU2ZmM2NjE4YiJdfSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZhY3ktc3RhZ2luZyIsImF1ZCI6ImZhY3ktc3RhZ2luZyIsImF1dGhfdGltZSI6MTY0MzI2OTYyMiwidXNlcl9pZCI6IlZLdlZUdEhzUDZnRG9NUW51MzVCbVpUNkVpMjIiLCJzdWIiOiJWS3ZWVHRIc1A2Z0RvTVFudTM1Qm1aVDZFaTIyIiwiaWF0IjoxNjQzMjY5NjIzLCJleHAiOjE2NDMyNzMyMjMsImVtYWlsIjoic3RnZGV2ZWxvcGVyK29yZ0BzdHlsZXIubGluayIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJzdGdkZXZlbG9wZXIrb3JnQHN0eWxlci5saW5rIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.8tIWYLod3sz1A1trZkNwrfLJWzWCWT0SVSw6PWR0l0B_pKEtMZVW181k01BiRyKmnUn6_RNtKt3-Bmx2Ze6-EZ3zZkFvj1AR7w9Sb0BfVc3-vAWb56zU7RnW_tB1fdY_NtBmsjE7CKmhwQ_lKc3p3IncrqpzZWJJE89hU0HVFCSKNzyM_girH-NYsaW9jo4isy4VGF_OaoSNfxDAcXTPK3VWr6NVoiOxixeViD62r0qODbwkxdrrKApM3RoAe1aYi0b4mW0DT1I_4BlBtT-WqCx3auIrcFve3Nd3ZR3i-t7z4jYjeQvbQLPG1D9zz2dth0n9e5sAy0neuoRA-WwNfQ'

        _ = await app.middleware_func(request, call_next)

        call_next.assert_called_once()

    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=True))
    async def test_missing_jwt(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development')
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = None

        response = await app.middleware_func(request, call_next)

        call_next.assert_not_called()
        assert isinstance(response, JSONResponse)
        assert response.status_code == 401

    @patch('styler_rest_framework.middlewares.fastapi.auth_middleware.validate', Mock(return_value=False))
    async def test_invalid_jwt(self):
        app = MockFastAPI()
        auth_middleware.add_auth_middleware(app, 'development')
        call_next = AsyncMock()
        request = Mock()
        request.headers.get.return_value = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjNhYTE0OGNkMDcyOGUzMDNkMzI2ZGU1NjBhMzVmYjFiYTMyYTUxNDkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoib3JnYW5pemF0aW9uIGFkbWluIChzdGcpIiwicm9sZXMiOlsiYWRtaW4iLCJzdGFmZiJdLCJjbGFpbXMiOnsib3JnYW5pemF0aW9uIjpbIjQxM2QzZjMwLTQxODUtNDJmZi05Mzc5LTIxZTdhNWQ1OWViNiIsIjhjZmI5YmJiLTgzODEtNGRjNC05ZmRhLTVmOTEyMTliYTM0YiJdLCJzaG9wIjpbImIxZDRlMzk2LWY4ZGEtNDU5Ni04MGE3LTJhNjdmZmI5MjIxZCIsImFhNDhmZjAyLTU3OGItNGQ2ZS05ZGM2LWNiM2FkYTc3NDg4NCIsImMzMWE2OWRlLWRhMDktNDUyNi05ZTkzLWE3ZjY5MDM3NWRhOCIsIjBlYWM0NTllLWZkZmEtNDRkNS1hZTViLWQ1YWVlNjRkNGY4MiIsImFlODAxMGIxLWM2MTYtNDdjYy1hNTE0LWQxOWZhM2E4NGQ1MiIsIjZmMWExN2JlLTFmODItNDVlNi04MDg5LWYzOTc4MWY4YWI0MSIsIjBiMWZhM2FjLTQ2OGQtNGM4ZS04YjhmLTQzY2Q1NjlkYjAxNSIsIjQ3ZmQ5MDYwLTc2ZDctNDQ4OC1iNTcyLTUxNTkyODNlOTEzYiIsImU3YzQyNzY1LTI5NWMtNDE5Yi04MTdjLWVlNzk5Y2U0MWYwYiIsIjY4YTVhYTM2LTA5NTYtNDJmNy1hOGEzLTkwZjJiYjg0ZWM1NCIsIjNhMmY1ZDAxLTJlYjItNDkyOS04Y2NjLWQwNTY0YWZkOWFjNiIsImRiMTQ3MmEyLTcwOGUtNDQ5Mi1hNzhiLTJhMDFjM2EwZjQ4ZCIsImZhZjNlMTJkLWY4NzMtNDhhZi1iNjNjLTM0ZmJhODJmMWFkOSIsImRlZDFjNDAyLTI4MGUtNDc4ZS1hMDY2LWNlNjk4YWEwYTIyZCIsIjdjZTAwZTRjLWU5M2QtNGE5Mi04ZTlkLTI1MDM0MWM2YWNlYSIsIjliMWY5MzhiLTVlMmMtNDVkYS1hNTc4LWZhNGZjNDUyZDhlZSIsIjBiNTVjMWQ4LThhZGQtNDljMy1iMTM5LTNhZmI1YWY5YTg1ZCIsIjRmYzA4ODY1LWUyNzUtNDFkOS05NzdiLTY1ZjE2ZjJiYTVkYSIsIjg5MTY0OTk1LTIyNzQtNDNlNC1hYTU1LTc1MWM3YmZjYmYzZCIsImU2YmYxNWNjLTJmZTUtNGUwYi04OWExLTY3NzNkNzZmMzc5YSIsIjMyNjM4ZDRhLTU3NGQtNDNlYS1hNGI5LTMzODIwYjIwYjFiZCIsImIxZmY2NTVmLTZjY2UtNGNiMC1hNWM2LTcwOWYzNmI5YjIxNCIsIjM3ZThmZGM1LTkwZDYtNDkxYi1iNzQ1LTIwZGRiNzAwZjUxMSIsIjY5ZjFiOWNhLTk2OTAtNDliOC1iMTAzLWUxYzYxNTUwMDhkMSIsIjJhZmE2NDkyLTc1MDItNGE0YS04MWE1LTc3NjgzNTZkODFiYiIsIjdjOTlmMWIyLTU3YWUtNDE1NS1iNzZkLWViZGNiMWNkNjc1OSIsImYxNWU2YTMyLTM0YmEtNGNkYi05NDFmLTJhYTE1ZDMyZjdlYSIsIjg1YTRkOTc1LTczZjgtNDNmYi05OTRlLWE0NjI4NDZlZDE4OCIsImI2OTIxNjM2LWYyNzctNDc2My04YmI4LWE0MjdlN2EwZDVkNiIsIjlhNGY2YWU5LTM2NWMtNDJhNy04MTJlLTEyYjU2ZmM2NjE4YiJdfSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZhY3ktc3RhZ2luZyIsImF1ZCI6ImZhY3ktc3RhZ2luZyIsImF1dGhfdGltZSI6MTY0MzI2OTYyMiwidXNlcl9pZCI6IlZLdlZUdEhzUDZnRG9NUW51MzVCbVpUNkVpMjIiLCJzdWIiOiJWS3ZWVHRIc1A2Z0RvTVFudTM1Qm1aVDZFaTIyIiwiaWF0IjoxNjQzMjY5NjIzLCJleHAiOjE2NDMyNzMyMjMsImVtYWlsIjoic3RnZGV2ZWxvcGVyK29yZ0BzdHlsZXIubGluayIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJzdGdkZXZlbG9wZXIrb3JnQHN0eWxlci5saW5rIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.8tIWYLod3sz1A1trZkNwrfLJWzWCWT0SVSw6PWR0l0B_pKEtMZVW181k01BiRyKmnUn6_RNtKt3-Bmx2Ze6-EZ3zZkFvj1AR7w9Sb0BfVc3-vAWb56zU7RnW_tB1fdY_NtBmsjE7CKmhwQ_lKc3p3IncrqpzZWJJE89hU0HVFCSKNzyM_girH-NYsaW9jo4isy4VGF_OaoSNfxDAcXTPK3VWr6NVoiOxixeViD62r0qODbwkxdrrKApM3RoAe1aYi0b4mW0DT1I_4BlBtT-WqCx3auIrcFve3Nd3ZR3i-t7z4jYjeQvbQLPG1D9zz2dth0n9e5sAy0neuoRA-WwNfQ'

        response = await app.middleware_func(request, call_next)

        call_next.assert_not_called()
        assert isinstance(response, JSONResponse)
        assert response.status_code == 401
