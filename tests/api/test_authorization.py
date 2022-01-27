
from styler_rest_framework.api.authorization import highest_role, authorize, Role


class TestHighestRole:
    def test_highest_role(self):
        roles = []
        assert highest_role(roles) == 0
        roles.append('staff')
        assert highest_role(roles) == 1
        roles.append('admin')
        assert highest_role(roles) == 2
        roles.append('sysadmin')
        assert highest_role(roles) == 4


class TestAuthorize:
    def test_return_decorator(self):
        assert callable(authorize(Role.ADMIN))


class TestDecorator:
    def test_minimum_role(self, token):

        @authorize(Role.ADMIN)
        def my_endpoint(authorization):
            return None

        tk = token(sysadmin=False, admin=False, staff=True)

        response = my_endpoint(authorization=f'Bearer {tk}')
        assert response.status_code == 403

        tk = token(sysadmin=False, admin=True, staff=True)
        response = my_endpoint(authorization=f'Bearer {tk}')
        assert response is None

        tk = token(sysadmin=True, admin=False, staff=True)
        response = my_endpoint(authorization=f'Bearer {tk}')
        assert response is None

    async def test_minimum_role_no_token(self, token):

        @authorize(Role.ADMIN)
        def my_endpoint():
            return None

        response = my_endpoint()
        assert response.status_code == 403

    async def test_minimum_role_async(self, token):

        @authorize(Role.ADMIN)
        async def my_endpoint(authorization):
            return None

        tk = token(sysadmin=False, admin=False, staff=True)

        response = await my_endpoint(authorization=f'Bearer {tk}')
        assert response.status_code == 403

        tk = token(sysadmin=False, admin=True, staff=True)
        response = await my_endpoint(authorization=f'Bearer {tk}')
        assert response is None

        tk = token(sysadmin=True, admin=False, staff=True)
        response = await my_endpoint(authorization=f'Bearer {tk}')
        assert response is None

    async def test_minimum_role_async_no_token(self, token):

        @authorize(Role.ADMIN)
        async def my_endpoint():
            return None

        response = await my_endpoint()
        assert response.status_code == 403
