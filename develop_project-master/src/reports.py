import datetime
import json
import logging
from typing import Any, Callable, Optional
import pandas as pd

# Настройка логирования
logger = logging.getLogger("report")
file_handler = logging.FileHandler("report.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def log_spending_by_category(filename: str) -> Callable:
    """Логирует результат функции в указанный файл."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            # Проверка на корректность результата перед записью в файл
            if isinstance(result, list):
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
            else:
                logger.error("Результат функции не является списком, не записываем в файл.")
            return result

        return wrapper

    return decorator


@log_spending_by_category("spending_by_category.json")
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> list:
    """Функция возвращающая траты за последние 3 месяца по заданной категории."""
    logger.info("Начало работы")

    # Преобразуем даты в DataFrame
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y", errors='coerce')

    if date is None:
        logger.info("Обработка условия на отсутствие даты")
        date_start = datetime.datetime.now() - datetime.timedelta(days=90)
        date_end = datetime.datetime.now()
    else:
        logger.info("Обработка условия с указанной датой")
        try:
            day, month, year = map(int, date.split("."))
            date_start = datetime.datetime(year, month, day) - datetime.timedelta(days=90)
            date_end = datetime.datetime(year, month, day)
        except ValueError as e:
            logger.error(f"Неверный формат даты: {e}")
            return []

    # Фильтрация по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата платежа"] >= date_start) &
        (transactions["Дата платежа"] <= date_end)
        ]

    logger.info("Завершение работы функции")
    result = filtered_transactions[["Сумма платежа", "Дата платежа", "Категория"]].to_dict(orient='records')

    # Проверка на корректность результата
    if not result:
        logger.warning("Нет транзакций для данной категории и периода.")

    return result

