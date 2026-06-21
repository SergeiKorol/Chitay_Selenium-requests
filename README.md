# Проект автоматизации тестирования Читай-город

## Описание проекта

Проект содержит набор автотестов для проверки функциональности поиска книг на сайте [Читай-город](https://www.chitai-gorod.ru/). Реализованы UI-тесты с использованием Selenium WebDriver и API-тесты для проверки эндпоинта поиска товаров.

**Задача:** автоматизировать проверку поиска книг по имени автора через веб-интерфейс и через API `web-gate`.

## Структура проекта

```plaintext
Chitay_Selenium-requests/
├── api/
│   ├── __init__.py
│   └── clients/
│       ├── __init__.py
│       └── auth_client.py    # Получение Bearer-токена для API
├── config/
│   ├── __init__.py
│   └── settings.py             # Настройки проекта (URL, пути API)
├── pages/
│   └── mainpage.py             # Page Object главной страницы
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Фикстура driver (Selenium)
│   ├── test_ui.py              # UI-тесты
│   └── test_api.py             # API-тесты
├── .github/
│   └── workflows/
│       └── api-tests.yml       # CI: ручной запуск API-тестов
├── .env.example                # Шаблон переменных окружения
├── conftest.py                 # Фикстура api_auth_headers
├── pytest.ini                  # Настройки pytest
├── requirements.txt            # Зависимости проекта
└── README.md                   # Документация
```

## Установка и настройка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/SergeiKorol/Chitay_Selenium-requests.git
cd Chitay_Selenium-requests
```

### 2. Создать и активировать виртуальное окружение

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить переменные окружения (опционально)

По умолчанию проект использует URL из `config/settings.py`. При необходимости их можно переопределить через переменные окружения:

```env
CHITAI_API_BASE_URL=https://web-gate.chitai-gorod.ru/api/v3
CHITAI_AUTH_BASE_URL=https://web-gate.chitai-gorod.ru/api/v1
CHITAI_ANONYMOUS_AUTH_PATH=/auth/anonymous
CHITAI_SITE_ORIGIN=https://www.chitai-gorod.ru
```

Для CI (GitHub Actions) рекомендуется задать готовый токен в секрете `CHITAI_ACCESS_TOKEN` — IP дата-центров часто блокируются DDoS-Guard при запросе `/auth/anonymous`.

Пример содержимого можно посмотреть в файле `.env.example`.

## Запуск тестов

### Запуск всех тестов

```bash
pytest -v -s
```

### Запуск только UI-тестов

```bash
pytest -m ui -v -s
```

### Запуск только API-тестов

```bash
pytest -m api -v -s
```

Альтернатива — запуск по файлу:

```bash
pytest tests/test_ui.py -v -s
pytest tests/test_api.py -v -s
```

## Запуск с Allure-отчётом

```bash
# Запуск тестов с сохранением результатов
pytest --alluredir=allure-results -v -s

# Генерация отчёта
allure generate allure-results -o allure-report --clean

# Открытие отчёта
allure open allure-report
```

## Содержание тестов

### UI-тесты (`tests/test_ui.py`)

| № | Тест | Описание |
|---|------|----------|
| 1 | `test_search_by_autor[Pushkin]` | Поиск по автору «Пушкин» → автор найден в результатах |
| 2 | `test_search_by_autor[Sumey_koch]` | Поиск по автору «Сумейе Коч» → автор найден в результатах |
| 3 | `test_search_by_autor[Stephen_king]` | Поиск по «Stephen King» → в результатах есть «Стивен Кинг» |

### API-тесты (`tests/test_api.py`)

| № | Тест | Описание |
|---|------|----------|
| 1 | `test_api_search` | GET `/search/product?phrase=запах смерти` → статус 200, фраза есть в ответе |

## CI (GitHub Actions)

Workflow `api-tests.yml` запускается вручную (`workflow_dispatch`) и выполняет API-тесты.

Перед первым запуском добавьте в **Settings → Secrets and variables → Actions** секрет:

- `CHITAI_ACCESS_TOKEN` — Bearer-токен, полученный локально:

```bash
python -c "from api.clients.auth_client import AuthClient; print(AuthClient.get_anonymous_access_token())"
```

## Технологии

- **Python** — язык программирования
- **pytest** — фреймворк для тестирования
- **Selenium WebDriver** — для UI-тестов
- **Requests** — для API-тестов
- **Allure** — для генерации отчётов

## Требования

- Python 3.8+
- Google Chrome (последняя версия)
- ChromeDriver (устанавливается автоматически через Selenium Manager в Selenium 4.6+)
- Allure CLI — для просмотра отчётов (опционально)
