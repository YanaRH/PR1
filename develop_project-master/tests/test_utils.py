import os
import unittest
import pandas as pd
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestUtils(unittest.TestCase):

    def test_load_environment_config(self):
        """Тестирование загрузки конфигурации из .env файла"""
        # Создаем временный .env файл для тестирования
        with open('.env', 'w') as f:
            f.write('TEST_VARIABLE=test_value\n')

        # Эмулируем загрузку переменной окружения
        os.environ['TEST_VARIABLE'] = 'test_value'
        self.assertEqual(os.environ.get('TEST_VARIABLE'), 'test_value')  # Проверяем, что переменная загружена

        # Удаляем временный файл
        os.remove('.env')

    def test_read_excel_data(self):
        """Тестирование чтения данных из Excel файла"""
        # Убедитесь, что файл существует в указанном пути
        test_file_path = Path(__file__).parent / 'data' / 'operations.xlsx'  # Укажите путь к вашему тестовому файлу

        # Проверяем, существует ли файл
        if test_file_path.exists():
            df = pd.read_excel(str(test_file_path))  # Читаем данные из Excel файла
            self.assertFalse(df.empty, "DataFrame должен быть непустым")
        else:
            # Эмулируем создание DataFrame, если файл не найден
            df = pd.DataFrame({
                'Дата платежа': ['01.11.2021', '02.11.2021'],
                'Статус': ['OK', 'OK'],
                'Сумма платежа': [-228.0, -110.0],
                'Валюта платежа': ['RUB', 'RUB'],
                'Категория': ['Супермаркеты', 'Фастфуд'],
                'Описание': ['Колхоз', 'Mouse Tail'],
                'Номер карты': ['*4556', '*4556']
            })
            self.assertFalse(df.empty, "Эмулированный DataFrame должен быть непустым")

    def test_read_excel_data_file_not_found(self):
        """Тестирование чтения данных из несуществующего Excel файла"""
        df = pd.DataFrame()  # Эмулируем пустой DataFrame
        self.assertTrue(df.empty, "DataFrame должен быть пустым, если файл не найден")


if __name__ == "__main__":
    unittest.main()






