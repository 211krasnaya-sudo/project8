markdown
# Catalog Project

Учебный проект: модели `Product` и `Category`, тесты `pytest`, покрытие кода, проверки качества
(flake8, black, isort, mypy).

Проект демонстрирует правильную структуру Python-пакета (`src/catalog`) и работу с Poetry,
что удобно переносить в Flask/Django проекты.

## Структура проекта

- `src/catalog/models.py классы `Product`, `Category` с атрибутами `name`, `description`, `price`, `quantity`.
- `tests/test_models.pyтесты на инициализацию, подсчёт количества продуктов и категорий.
- `pyproject.toml зависимости и конфигурация Poetry.
- `.gitignor исключает виртуальное окружение, кэш тестов и отчёты покрытия.

## Установка

```bash
poetry install
