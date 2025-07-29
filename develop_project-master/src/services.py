import json
import logging
import pandas as pd  # Импортируем pandas

# Импортируем декоратор из текущего пакета
from .decorators import decorator_search  # Относительный импорт

# Настройка логирования
logger = logging.getLogger("services")
file_handler = logging.FileHandler("services.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


@decorator_search
def simple_search(transactions: pd.DataFrame, string_search: str) -> str:
    """Функция поиска по переданной строке в DataFrame."""
    result = []
    logger.info("Начало работы функции (simple_search)")

    if not string_search:
        logger.warning("Пустая строка для поиска")
        return json.dumps(result, indent=4, ensure_ascii=False)

    # Фильтрация данных
    for index, row in transactions.iterrows():
        # Проверка на наличие значений в столбцах
        if pd.isna(row["Описание"]) or pd.isna(row["Категория"]):
            continue

        # Поиск в описании и категории
        if string_search in row["Описание"] or string_search in row["Категория"]:
            result.append(row.to_dict())  # Преобразуем строку DataFrame в словарь

    logger.info("Конец работы функции (simple_search)")
    data_json = json.dumps(result, indent=4, ensure_ascii=False)

    return data_json



