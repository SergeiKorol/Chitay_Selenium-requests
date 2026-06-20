import pytest
import allure
from selenium.common import TimeoutException

from pages.mainpage import Mainpage

def test_search_by_phrase(driver):
    """
    Проверяем что в результатах поиска есть искомый автор.
    1. В строке поиска пишем автора
    2. Запускаем поиск
    3. Собираем результаты
    4. Находим авторов первых 5 книг
    5. Проверяем что искомый автор есть среди результатов
    """
    main = Mainpage(driver)
    search_phrase = "Сумейе Коч"

    with allure.step("Перейти на сайт Читай-город"):
        main.open_main()

    with allure.step(f"Найти книгу по фразе {search_phrase}"):

        main.search_by_phrase(search_phrase)

    with allure.step("Проверить, что результаты поиска отображаются"):
        try:
            results = main.get_search_results()
            assert len(results) > 0, "Результаты поиска не найдены"
            allure.attach(f"Найдено результатов: {len(results)}",
                          "Количество результатов",
                          allure.attachment_type.TEXT)
        except TimeoutException:
            assert False, ("Результаты поиска"
                           " не загрузились в течение 10 секунд")

    with allure.step("Получить авторов из результатов поиска"):
        authors = main.get_authors_from_results()
        allure.attach(f"Найдено авторов: {len(authors)}",
                      "Количество авторов", allure.attachment_type.TEXT)

        if authors:
            allure.attach("\n".join(authors[:5]),
                          "Первые 5 авторов", allure.attachment_type.TEXT)

    with allure.step("Проверить, что искомай автор"
                     " присутствует в результатах"):

        phrase_found = False

        # Проверяем среди авторов
        for author in authors:
            if search_phrase.lower() in author.lower():
                phrase_found = True
                allure.attach(f"Найдена фраза у автора: {author}",
                              "Фраза найдена", allure.attachment_type.TEXT)
                break
        assert phrase_found == True