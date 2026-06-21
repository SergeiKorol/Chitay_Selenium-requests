"""Клиент для получения Bearer-токена Читай-город."""

import requests

from config import settings


class AuthClient:
    """Получает анонимный access token для API Читай-город."""

    @staticmethod
    def resolve_access_token() -> str:
        """
        Возвращает access token для API-запросов.

        Если задан ``CHITAI_ACCESS_TOKEN``, используется он (удобно для CI).
        Иначе токен запрашивается у ``/auth/anonymous``.

        Returns:
            Строка токена. Может уже содержать префикс ``Bearer``.

        Raises:
            requests.HTTPError: Если сервис авторизации вернул ошибку.
            KeyError: Если в ответе нет поля ``token.accessToken``.
            ValueError: Если токен пустой.
        """
        if settings.ACCESS_TOKEN:
            return settings.ACCESS_TOKEN.strip()

        return AuthClient.get_anonymous_access_token()

    @staticmethod
    def get_anonymous_access_token() -> str:
        """
        Запрашивает свежий анонимный Bearer-токен.

        Перед auth-запросом открывает главную страницу сайта в той же
        HTTP-сессии, чтобы получить cookies DDoS-Guard (как делает браузер).

        Returns:
            Строка токена. Может уже содержать префикс ``Bearer``.

        Raises:
            requests.HTTPError: Если сервис авторизации вернул ошибку.
            KeyError: Если в ответе нет поля ``token.accessToken``.
        """
        session = requests.Session()
        session.headers.update(AuthClient._default_headers())

        session.get(f"{settings.SITE_ORIGIN}/", timeout=20)

        response = session.post(
            url=f"{settings.AUTH_BASE_URL}{settings.ANONYMOUS_AUTH_PATH}",
            timeout=20,
        )
        if response.status_code == 403:
            raise requests.HTTPError(
                "403 Forbidden при запросе анонимного токена. "
                "Частая причина в CI — блокировка IP дата-центра (DDoS-Guard). "
                "Получите токен локально и добавьте его в GitHub Secrets "
                "как CHITAI_ACCESS_TOKEN.",
                response=response,
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
            access_token: Токен из ``resolve_access_token``.

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
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": settings.SITE_ORIGIN,
            "referer": f"{settings.SITE_ORIGIN}/",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
        }
