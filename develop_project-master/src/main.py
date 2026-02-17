import json
import logging
from pathlib import Path
import pandas as pd
import http.client
import os
import configparser


# Класс для загрузки переменных окружения из .env файла
class EnvConfig:
    def __init__(self):
        self.env_file = Path('.env')
        self.config = configparser.ConfigParser()
        self._load_env()
        self._load_config()

    def _load_env(self):
        """Загружает переменные окружения из .env файла"""
        if not self.env_file.exists():
            print(f"Файл {self.env_file} не найден!")
            return

        with open(self.env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    if (value.startswith('"') and value.endswith('"')) or \
                            (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    os.environ[key] = value
                except ValueError as e:
                    print(f"Ошибка в строке .env: {line}")

    def _load_config(self):
        """Загружает конфигурацию из config.ini"""
        config_file = Path('config.ini')
        if config_file.exists():
            self.config.read(config_file)

    def get(self, key, default=None):
        """Получает значение из переменных окружения или конфига"""
        return os.getenv(key) or self.config.get('DEFAULT', key, fallback=default)


# Настройка логирования
logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("main.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# Инициализация конфигурации
env = EnvConfig()


# Функция для получения информации о текущих акциях
def get_stock_info() -> dict:
    """Возвращает информацию о текущих акциях."""
    api_key = env.get("ALPHA_VANTAGE_API_KEY")  # Получаем ключ из .env
    conn = http.client.HTTPSConnection("www.alphavantage.co")
    url = f"/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey={api_key}"

    try:
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            logger.error(f"Ошибка при получении данных о акциях: {response.status} {response.reason}")
            return {}

        stock_data = json.loads(response.read().decode())
        time_series = stock_data.get("Time Series (5min)", {})

        # Обработка данных для возврата
        if time_series:
            latest_time = next(iter(time_series))
            return {
                "AAPL": {
                    "price": float(time_series[latest_time]["1. open"]),
                    "change": float(time_series[latest_time]["4. close"]) - float(time_series[latest_time]["1. open"])
                }
            }
        else:
            logger.warning("Нет данных о временных рядах акций.")
            return {}
    except Exception as e:
        logger.error(f"Ошибка при получении данных о акциях: {e}")
        return {}
    finally:
        conn.close()


# Функция для получения текущих валютных курсов
def get_currency_rates() -> dict:
    """Возвращает текущие валютные курсы."""
    api_key = env.get("EXCHANGE_RATE_API_KEY")  # Получаем ключ из .env
    conn = http.client.HTTPSConnection("open.er-api.com")
    url = f"/v6/{api_key}/latest/USD"  # Пример запроса для получения курсов относительно USD

    try:
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            logger.error(f"Ошибка при получении данных о валютных курсах: {response.status} {response.reason}")
            return {}

        currency_data = json.loads(response.read().decode())

        # Возвращаем курсы валют
        return currency_data.get("rates", {})
    except Exception as e:
        logger.error(f"Ошибка при получении данных о валютных курсах: {e}")
        return {}
    finally:
        conn.close()


# Чтение Excel файла в DataFrame
def read_excel(file_path: str) -> pd.DataFrame:
    """Чтение Excel файла и возврат DataFrame."""
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        raise


# Функция для обработки транзакций и получения информации по картам
def for_each_card(transactions: pd.DataFrame) -> list:
    """Возвращает список уникальных карт из транзакций."""
    if 'card_number' not in transactions.columns:
        logger.warning("Столбец 'card_number' отсутствует в DataFrame.")
        return []
    cards = transactions['card_number'].unique().tolist()
    return cards


# Функция для получения топ-5 транзакций
def top_five_transaction(transactions: pd.DataFrame) -> list:
    """Возвращает топ-5 транзакций по сумме."""
    if 'amount' not in transactions.columns:
        logger.warning("Столбец 'amount' отсутствует в DataFrame.")
        return []
    top_transactions = transactions.nlargest(5, 'amount')
    return top_transactions.to_dict(orient='records')


def filter_by_date(start_date, end_date, transactions):
    column_name = 'Дата операции'
    if column_name not in transactions.columns:
        print("Столбец 'Дата операции' не найден. Доступные столбцы:", list(transactions.columns))
        raise KeyError("Столбец 'Дата операции' отсутствует.")

    # Исправленный парсинг для формата гггг-мм-дд
    transactions[column_name] = pd.to_datetime(transactions[column_name], format='%Y-%m-%d', errors='coerce')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_transactions = transactions[
        (transactions[column_name] >= start_date) & (transactions[column_name] <= end_date)]
    return filtered_transactions

# Путь к файлу
file_path = str(Path(__file__).resolve().parent.parent / "data" / "operations.xlsx")
data_frame = read_excel(file_path)


def main(start_date: str, end_date: str, df_transactions: pd.DataFrame) -> str:
    """Функция создающая JSON ответ для страницы главная."""
    logger.info("Начало работы главной функции (main)")
    final_list = filter_by_date(start_date, end_date, df_transactions)

    cards = for_each_card(final_list)
    top_trans = top_five_transaction(final_list)

    # Получаем информацию о текущих акциях и валютных курсах
    stock_info = get_stock_info()
    currency_rates = get_currency_rates()

    logger.info("Создание JSON ответа")
    result = [{
        "cards": cards,
        "top_transactions": top_trans,
        "stock_info": stock_info,
        "currency_rates": currency_rates,
    }]

    date_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )
    logger.info("Завершение работы главной функции (main)")
    return date_json


# Пример вызова функции main
if __name__ == "__main__":
    start_date = "2025-01-01"
    end_date = "2025-12-31"
    main(start_date, end_date, data_frame)




