import json
import logging
from pathlib import Path
import pandas as pd  # Импортируем pandas для работы с DataFrame
import http.client  # Импортируем http.client для работы с HTTP-запросами
import urllib.parse  # Импортируем urllib для кодирования URL

# Настройка логирования
logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("main.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

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

# Функция для фильтрации транзакций по дате
def filter_by_date(start_date: str, end_date: str, transactions: pd.DataFrame) -> pd.DataFrame:
    """Фильтрация транзакций по заданному диапазону дат."""
    if transactions.empty:
        logger.warning("DataFrame пустой.")
        return transactions  # Если DataFrame пустой, возвращаем его

    # Преобразуем строки дат в формат datetime
    start_date = pd.to_datetime(start_date, errors='coerce')
    end_date = pd.to_datetime(end_date, errors='coerce')

    if pd.isna(start_date) or pd.isna(end_date):
        logger.error("Некорректный формат даты")
        raise ValueError("Некорректный формат даты")

    # Фильтруем транзакции по диапазону дат
    filtered_transactions = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]
    return filtered_transactions

# Функция для получения информации о текущих акциях
def get_stock_info() -> dict:
    """Возвращает информацию о текущих акциях."""
    conn = http.client.HTTPSConnection("api.example.com")
    url = "/stocks"  # Замените на реальный путь API
    try:
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            logger.error(f"Ошибка при получении данных о акциях: {response.status} {response.reason}")
            return {}

        stock_data = json.loads(response.read().decode())  # Предполагается, что API возвращает JSON

        # Пример обработки данных, измените в соответствии с форматом ответа API
        return {
            stock['symbol']: {
                "price": stock['price'],
                "change": stock['change']
            } for stock in stock_data
        }
    except Exception as e:
        logger.error(f"Ошибка при получении данных о акциях: {e}")
        return {}
    finally:
        conn.close()

# Функция для получения текущих валютных курсов
def get_currency_rates() -> dict:
    """Возвращает текущие валютные курсы."""
    conn = http.client.HTTPSConnection("api.example.com")
    url = "/currency"  # Замените на реальный путь API
    try:
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            logger.error(f"Ошибка при получении данных о валютных курсах: {response.status} {response.reason}")
            return {}

        currency_data = json.loads(response.read().decode())  # Предполагается, что API возвращает JSON

        # Пример обработки данных, измените в соответствии с форматом ответа API
        return {
            currency['code']: currency['rate'] for currency in currency_data
        }
    except Exception as e:
        logger.error(f"Ошибка при получении данных о валютных курсах: {e}")
        return {}
    finally:
        conn.close()

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



