import sys

sys.path.append('src')

import os
from dotenv import load_dotenv
from main import main, filter_by_date, read_excel
from pathlib import Path
import pandas as pd

load_dotenv()


def run_all_functionalities():
    # Загрузка данных
    transactions_file = os.getenv('TRANSACTIONS_FILE', 'data/operations.xlsx')
    start_date = os.getenv('START_DATE', '2018-01-01')
    end_date = os.getenv('END_DATE', '2021-12-31')

    try:
        df_transactions = read_excel(transactions_file)
        print(f"Данные загружены: {len(df_transactions)} строк.")

        # Отладка: проверьте даты перед фильтрацией (гибкий парсинг)
        if 'Дата операции' in df_transactions.columns:
            df_transactions['Дата операции'] = pd.to_datetime(df_transactions['Дата операции'],
                                                              errors='coerce')  # Убрал format для авто-парсинга
            min_date = df_transactions['Дата операции'].min()
            max_date = df_transactions['Дата операции'].max()
            print(f"Минимальная дата в файле: {min_date}")
            print(f"Максимальная дата в файле: {max_date}")
            print(f"Диапазон фильтрации: {start_date} to {end_date}")
            print("Первые 5 значений столбца 'Дата операции':")
            print(df_transactions['Дата операции'].head())  # Диагностика
        else:
            print("Столбец 'Дата операции' не найден.")
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return

    # Фильтрация
    try:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        filtered = filter_by_date(start_dt, end_dt, df_transactions)
        print(f"Фильтрация по дате: {len(filtered)} транзакций.")
        if len(filtered) == 0:
            print("Диапазон дат не покрывает данные. Скорректируйте START_DATE/END_DATE в .env на основе мин/макс дат.")
    except Exception as e:
        print(f"Ошибка фильтрации: {e}")
        return

    # Главная функция (JSON)
    try:
        result_json = main(start_date, end_date, df_transactions)
        print("Результат главной функции (JSON):")
        print(result_json)
    except Exception as e:
        print(f"Ошибка в главной функции: {e}")


if __name__ == "__main__":
    run_all_functionalities()