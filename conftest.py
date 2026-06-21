import pytest

from api.clients.auth_client import AuthClient


@pytest.fixture(scope="session")
def api_auth_headers() -> dict[str, str]:
    """
    Возвращает свежие заголовки авторизации для API-тестов.

    Токен запрашивается один раз на всю pytest-сессию.
    """
    access_token = AuthClient.resolve_access_token()
    return AuthClient.build_authorization_headers(access_token)
