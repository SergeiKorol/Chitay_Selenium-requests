import pytest


@pytest.fixture(scope="function")
def driver():
    """Подготавливает браузер для UI-тестов."""
    from selenium import webdriver

    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()
