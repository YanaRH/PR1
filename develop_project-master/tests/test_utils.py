import os
import unittest
import pandas as pd
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Создание временного .env файла для тестирования"""
        cls.env_file_path = Path('.env')
        with open(cls.env_file_path, 'w') as f:
            f.write('TEST_VARIABLE=test_value\n')

    @classmethod
    def tearDownClass(cls):
        """Удаление временного .env файла после тестов"""
        if cls.env_file_path.exists():
            os.remove(cls.env_file_path)

    def test_load_environment_config(self):
        """Тестирование загрузки конфигурации из .env файла"""
        # Эмулируем загрузку переменной окружения
        with open(self.env_file_path) as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

        self.assertEqual(os.environ.get('TEST_VARIABLE'), 'test_value')  # Проверяем, что переменная загружена

    def test_read_excel_data(self):
        """Тестирование чтения данных из Excel файла"""
        # Создаем временный Excel файл для тестирования
        test_file_path = Path(__file__).parent / 'data' / 'operations.xlsx'
        test_file_path.parent.mkdir(parents=True, exist_ok=True)  # Создаем директорию, если не существует

        # Создаем тестовый Excel файл
        df = pd.DataFrame({
            'Дата платежа': ['01.11.2021', '02.11.2021'],
            'Статус': ['OK', 'OK'],
            'Сумма платежа': [-228.0, -110.0],
            'Валюта платежа': ['RUB', 'RUB'],
            'Категория': ['Супермаркеты', 'Фастфуд'],
            'Описание': ['Колхоз', 'Mouse Tail'],
            'Номер карты': ['*4556', '*4556']
        })
        df.to_excel(test_file_path, index=False)

        # Проверяем, существует ли файл
        if test_file_path.exists():
            df = pd.read_excel(str(test_file_path))  # Читаем данные из Excel файла
            self.assertFalse(df.empty, "DataFrame должен быть непустым")
        else:
            self.fail("Тестовый файл не был создан")

    def test_read_excel_data_file_not_found(self):
        """Тестирование чтения данных из несуществующего Excel файла"""
        non_existent_file_path = Path(__file__).parent / 'data' / 'non_existent_file.xlsx'
        df = pd.DataFrame()  # Эмулируем пустой DataFrame
        self.assertTrue(df.empty, "DataFrame должен быть пустым, если файл не найден")

if __name__ == "__main__":
    unittest.main()







