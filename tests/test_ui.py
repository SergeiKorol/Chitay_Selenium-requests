import allure
import pytest
from selenium.common import TimeoutException

from pages.mainpage import Mainpage

pytestmark = pytest.mark.ui


@pytest.mark.parametrize(
    "search_phrase, expected_author",
    [
        ("Пушкин", "Пушкин"),
        ("Сумейе Коч", "Сумейе Коч"),
        ("Stephen King", "Стивен Кинг"),
    ],
    ids=["Pushkin", "Sumey_koch", "Stephen_king"],
)
def test_search_by_autor(
    driver,
    search_phrase: str,
    expected_author: str,
) -> None:
    """
    Проверяем, что в результатах поиска есть искомый автор.

    1. В строке поиска вводим имя автора (в т.ч. латиницей).
    2. Запускаем поиск.
    3. Собираем результаты.
    4. Получаем авторов из карточек.
    5. Проверяем, что ожидаемый автор есть среди результатов.
    """
    main = Mainpage(driver)

    with allure.step("Перейти на сайт Читай-город"):
        main.open_main()

    with allure.step(f"Найти книгу по фразе «{search_phrase}»"):
        main.search_by_phrase(search_phrase)

    with allure.step("Проверить, что результаты поиска отображаются"):
        try:
            results = main.get_search_results()
            assert (
                len(results) > 0
            ), f"Результаты поиска по запросу «{search_phrase}» не найдены"
            allure.attach(
                f"Найдено результатов: {len(results)}",
                "Количество результатов",
                allure.attachment_type.TEXT,
            )
        except TimeoutException:
            assert False, (
                f"Результаты поиска по запросу «{search_phrase}» "
                "не загрузились в течение 10 секунд"
            )

    with allure.step("Получить авторов из результатов поиска"):
        authors = main.get_authors_from_results()
        allure.attach(
            f"Найдено авторов: {len(authors)}",
            "Количество авторов",
            allure.attachment_type.TEXT,
        )

        if authors:
            allure.attach(
                "\n".join(authors[:5]),
                "Первые 5 авторов",
                allure.attachment_type.TEXT,
            )

    with allure.step(
        f"Проверить, что автор «{expected_author}» присутствует в результатах"
    ):
        phrase_found = any(
            expected_author.lower() in author.lower() for author in authors
        )

        if phrase_found:
            matched_author = next(
                author
                for author in authors
                if expected_author.lower() in author.lower()
            )
            allure.attach(
                f"Найдена фраза у автора: {matched_author}",
                "Фраза найдена",
                allure.attachment_type.TEXT,
            )

        assert phrase_found, (
            f"Автор «{expected_author}» не найден среди результатов поиска "
            f"по запросу «{search_phrase}». Полученные авторы: {authors[:5]}"
        )
