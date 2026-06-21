from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Mainpage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    MAIN_PAGE_URL = "https://www.chitai-gorod.ru/"

    # Поле поиска на главной странице
    INPUT = "//input[@id='app-search']"

    # Кнопка отправки поискового запроса в форме поиска
    SEARCH = "//button[@type='submit' and @aria-label='Найти']"

    # Первая книга в списке результатов.
    FIRST_BOOK = (
        '//article[@class="product-card product-card__view-type--base '
        'app-products-list__item"][1]'
    )

    # Кнопка "Купить" на карточке товара.
    BUY_BUTTON = '//button[@data-testid-button-mini-product-card="canBuy"]'

    # Кнопка "Оформить"(появляется после добавления в корзину).
    OFORMIT_BUTTON = '//div[text()=" Оформить"]'

    # Индикатор количества товаров в корзине.
    CART_COUNT = "//div[@data-testid-indicator-header]"

    # Кнопка\иконка корзины для перехода.
    CART_BUTTON = '//button[@aria-label="Корзина"]'

    # Кнопка очистки всей корзины.
    CLEAR_CART_BUTTON = '//button[@data-testid-button-cart="clearAll"]'

    # Сообщение об успешной очистке корзины.
    MESSAGE_CLEARED_CART = '//p[@class="cart-multiple-delete__title"]'

    # Страница с результатами
    RESULT_PAGE = '//div[@class="search-page"]'

    def open_main(self):
        self.driver.get(self.MAIN_PAGE_URL)
        self.close_overlays()

    def close_overlays(self) -> None:
        """Закрывает баннер, Ваш город который перекрывает клик по поиску."""
        short_wait = WebDriverWait(self.driver, 2)
        overlay_button = "//button[contains(., 'Да, я здесь')]"

        try:
            button = short_wait.until(
                EC.element_to_be_clickable((By.XPATH, overlay_button))
            )
            button.click()
        except (TimeoutException, StaleElementReferenceException):
            pass

    def _wait_for_search_results_page(self) -> None:
        """Ждёт загрузки страницы результатов поиска."""
        self.wait.until(EC.url_contains("/search"))
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.RESULT_PAGE))
        )

    def search_by_phrase(self, frase) -> None:
        """
        Поиск по фразе через строку поиска.

        Сначала отправляет запрос через Enter, при неудаче повторяет клик
        по кнопке «Найти».
        """
        self.close_overlays()

        input_element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.INPUT))
        )
        input_element.click()
        input_element.clear()
        input_element.send_keys(frase)
        input_element.send_keys(Keys.ENTER)

        try:
            self._wait_for_search_results_page()
            return
        except TimeoutException:
            pass

        search_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.SEARCH))
        )

        search_button.click()
        self._wait_for_search_results_page()

    def get_search_results(self):
        """Получить все результаты поиска"""
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//article[contains(@class, 'product-card')]")
            )
        )
        return self.driver.find_elements(
            By.XPATH, "//article[contains(@class, 'product-card')]"
        )

    def get_authors_from_results(self):
        """Получить список авторов из результатов поиска"""
        authors_elements = self.driver.find_elements(
            By.XPATH, "//span[@class='product-card__subtitle']"
        )
        return [author.text for author in authors_elements if author.text]

    def get_book_titles_from_results(self):
        """Получить список названий книг из результатов поиска"""
        titles_elements = self.driver.find_elements(
            By.XPATH, "//div[@class='product-card__title']"
        )
        return [title.text for title in titles_elements if title.text]

    def is_no_results_message_displayed(self):
        """Проверить, отображается ли сообщение об отсутствии результатов"""
        try:
            no_results = self.driver.find_element(
                By.XPATH,
                "//div[contains(text(),"
                "ничего не нашлось') "
                "or contains(text(), 'не найдено')]",
            )
            return no_results.is_displayed()
        except:
            return False

    def add_first_book_to_cart(self):
        """Добавить первую книгу в результатах поиска в корзину"""
        try:
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.ADD_TO_CART_BUTTON))
            )
            add_button.click()
            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        "//article[contains(@class,"
                        " 'product-card')],"
                        " 'loading')]",
                    )
                )
            )
            return True
        except Exception as e:
            print(f"Не удалось добавить книгу в корзину: {e}")
            return False

    def get_first_book_title(self):
        """Получить название первой книги в результатах поиска"""
        try:
            title_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='product-card__title']")
                )
            )
            return title_element.text
        except:
            return None

    def go_to_cart(self):
        """Перейти в корзину"""
        cart_icon = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.CART_ICON))
        )
        cart_icon.click()
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Корзина')]")
            )
        )

    def get_cart_items(self):
        """Получить все товары в корзине"""
        try:
            return self.driver.find_elements(By.XPATH, self.CART_ITEM)
        except:
            return []

    def get_cart_item_titles(self):
        """Получить названия товаров в корзине"""
        try:
            title_elements = self.driver.find_elements(
                By.XPATH, self.CART_ITEM_TITLE
            )
            return [title.text for title in title_elements if title.text]
        except:
            return []

    def remove_first_item_from_cart(self):
        """Удалить первый товар из корзины"""
        try:
            remove_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, self.REMOVE_FROM_CART_BUTTON)
                )
            )
            remove_button.click()
            self.wait.until(
                EC.invisibility_of_element_located((By.XPATH, self.CART_ITEM))
            )
            return True
        except:
            return False

    def is_cart_empty(self):
        """Проверить, пуста ли корзина"""
        try:
            empty_message = self.driver.find_element(
                By.XPATH, self.EMPTY_CART_MESSAGE
            )
            return empty_message.is_displayed()
        except:
            items = self.get_cart_items()
            return len(items) == 0

    def go_to_book(self, book_url):
        """Получает книгу по book_url"""
        self.driver.get(book_url)

    def buy_current_book(self):
        """Нажимает на кнопку 'Купить'"""
        button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.BUY_BUTTON))
        )
        button.click()

    def is_button_oformit(self):
        """Появляется название кнопки 'Оформить'"""
        if self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.OFORMIT_BUTTON))
        ):
            return True
        else:
            return False

    def get_cart_count(self):
        """Получает количество книг в корзине"""
        count = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.CART_COUNT))
        )
        return int(count.text)

    def click_cart(self):
        """Нажимает на кнопку 'Корзина'"""
        button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.CART_BUTTON))
        )
        button.click()

    def clear_cart_items(self):
        """Нажимает на кнопку 'Очистить корзину'"""
        button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.CLEAR_CART_BUTTON))
        )
        button.click()

    def is_cleared_cart_message(self):
        """Сообщает об успешной очистке корзины"""
        if self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.MESSAGE_CLEARED_CART))
        ):
            return True
        else:
            return False
