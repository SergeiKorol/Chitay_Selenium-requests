import allure
import pytest
import requests

from config import settings

pytestmark = pytest.mark.api


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.story("Поиск по ключевым словам")
@allure.title("Поиск книги по названию")
@allure.description("Тест проверяет успешный поиск книги по названию")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_search(api_auth_headers: dict[str, str]) -> None:
    book = "Метро"

    with allure.step("Подготовка тестовых данных"):
        search_params = {"phrase": book}

    with allure.step(
        f"Выполнение GET запроса "
        f"к /search/product с параметром phrase={book}"
    ):
        response = requests.get(
            url=f"{settings.API_BASE_URL}/search/product",
            params=search_params,
            headers=api_auth_headers,
            timeout=20,
        )

    with allure.step("Проверка статус кода ответа"):
        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}: "
            f"{response.text[:300]}"
        )
        allure.attach(
            str(response.status_code),
            "Status Code",
            allure.attachment_type.TEXT,
        )

    with allure.step("Проверка наличия поисковой фразы в ответе"):
        attributes = response.json()["data"]["attributes"]
        transformed_phrase = attributes.get("transformedPhrase", "")
        seo_title = attributes.get("seo", {}).get("title", "")

        phrase_found = (
            book.lower() in transformed_phrase.lower()
            or book.lower() in seo_title.lower()
        )

        allure.attach(
            transformed_phrase or seo_title,
            "Поисковая фраза в ответе",
            allure.attachment_type.TEXT,
        )

        assert phrase_found, (
            f"Фраза «{book}» не найдена в ответе API. "
            f"transformedPhrase={transformed_phrase!r}, seo.title={seo_title!r}"
        )
