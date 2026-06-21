"""Конфигурация окружения для API-тестов."""

import os

API_BASE_URL: str = os.getenv(
    "CHITAI_API_BASE_URL",
    "https://web-gate.chitai-gorod.ru/api/v3",
)
AUTH_BASE_URL: str = os.getenv(
    "CHITAI_AUTH_BASE_URL",
    "https://web-gate.chitai-gorod.ru/api/v1",
)
ANONYMOUS_AUTH_PATH: str = os.getenv(
    "CHITAI_ANONYMOUS_AUTH_PATH",
    "/auth/anonymous",
)
SITE_ORIGIN: str = os.getenv(
    "CHITAI_SITE_ORIGIN",
    "https://www.chitai-gorod.ru",
)
ACCESS_TOKEN: str | None = os.getenv("CHITAI_ACCESS_TOKEN")
