"""Клиент для получения Bearer-токена Читай-город."""

import requests

from config import settings


class AuthClient:
    """Получает анонимный access token для API Читай-город."""

    @staticmethod
    def get_anonymous_access_token() -> str:
        """
        Запрашивает свежий анонимный Bearer-токен.

        Returns:
            Строка токена. Может уже содержать префикс ``Bearer``.

        Raises:
            requests.HTTPError: Если сервис авторизации вернул ошибку.
            KeyError: Если в ответе нет поля ``token.accessToken``.
        """
        response = requests.post(
            url=f"{settings.AUTH_BASE_URL}{settings.ANONYMOUS_AUTH_PATH}",
            headers=AuthClient._default_headers(),
            timeout=20,
        )
        response.raise_for_status()

        access_token = response.json()["token"]["accessToken"]
        if not access_token:
            raise ValueError("Сервис авторизации вернул пустой accessToken")

        return access_token

    @staticmethod
    def build_authorization_headers(access_token: str) -> dict[str, str]:
        """
        Собирает заголовки авторизации для API-запросов.

        Args:
            access_token: Токен из ``get_anonymous_access_token``.

        Returns:
            Словарь HTTP-заголовков для запросов к web-gate API.
        """
        authorization_value = (
            access_token
            if access_token.startswith("Bearer ")
            else f"Bearer {access_token}"
        )

        return {
            **AuthClient._default_headers(),
            "authorization": authorization_value,
        }

    @staticmethod
    def _default_headers() -> dict[str, str]:
        """Возвращает браузероподобные заголовки для auth-запроса."""
        return {
            "accept": "application/json",
            "origin": settings.SITE_ORIGIN,
            "referer": f"{settings.SITE_ORIGIN}/",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
        }
