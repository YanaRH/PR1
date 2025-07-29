import os
import pandas as pd  # Основной импорт pandas
from pathlib import Path


def load_environment_config():
    """Загрузка конфигурации из .env файла"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass


def read_excel_data(file_path: str) -> pd.DataFrame:
    """Чтение данных из Excel файла с обработкой ошибок"""
    try:
        # Установите openpyxl: pip install openpyxl
        data = pd.read_excel(file_path, engine='openpyxl')
        return data
    except Exception as e:
        print(f"Ошибка чтения Excel: {str(e)}")
        return pd.DataFrame()


# Основной код
if __name__ == "__main__":
    # Загружаем конфигурацию
    load_environment_config()

    # Указываем корректный путь к файлу
    excel_path = Path(__file__).parent.parent / 'data' / 'operations.xlsx'

    # Читаем данные
    try:
        df = read_excel_data(str(excel_path))
        print(f"Успешно загружено {len(df)} записей")
    except Exception as e:
        print(f"Фатальная ошибка: {str(e)}")

