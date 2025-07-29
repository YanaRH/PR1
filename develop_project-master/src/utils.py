import json
import logging
from typing import List, Dict, Any, Optional
import pandas as pd  # Используем pandas для чтения Excel
from urllib.request import urlopen
import configparser  # Используем configparser для конфигурации

# Настройка конфигурации
config = configparser.ConfigParser()
config.read('config.ini')  # Читаем конфиг из файла

# Получение конфигурационных ключей
CURRENCY_API_KEY = config.get('DEFAULT', 'API_KEY_CUR', fallback="")
STOCK_API_KEY = config.get('DEFAULT', 'SP_500_API_KEY', fallback="")

# Конфигурация логирования
logger = logging.getLogger("application")
handler = logging.FileHandler("application.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def read_excel_data(file_path: str) -> pd.DataFrame:
    """Чтение Excel-файла с использованием pandas."""
    try:
        data = pd.read_excel(file_path, engine='openpyxl')  # Чтение Excel файла
        logger.info(f"Успешно прочитан файл: {file_path}")
        return data
    except Exception as e:
        logger.error(f"Ошибка чтения файла: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки

def http_request(url: str) -> Any:
    """Выполняет HTTP-запрос и возвращает ответ."""
    try:
        with urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        logger.error(f"HTTP ошибка: {e}")
        return None

def fetch_data_from_file(file_path: str) -> pd.DataFrame:
    """Загружает данные из файла и возвращает DataFrame."""
    return read_excel_data(file_path)

# Пример использования
if __name__ == "__main__":
    # Загрузка данных
    data = fetch_data_from_file("data/operations.xlsx")  # Загрузка данных из Excel

    # HTTP-запрос
    api_response = http_request("https://api.example.com/data")

    # Логирование
    logger.info("Приложение успешно запущено")
