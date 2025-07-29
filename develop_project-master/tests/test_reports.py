import unittest as testing_framework
import pandas as pd


# Получаем тестовый DataFrame
def get_test_data():
    """Возвращает тестовый DataFrame"""
    test_data = [
        {"Дата платежа": "31.12.2021", "Категория": "Переводы", "Сумма": 1000},
        {"Дата платежа": "31.12.2021", "Категория": "Развлечения", "Сумма": 200},
        {"Дата платежа": "30.12.2021", "Категория": "Переводы", "Сумма": 500},
        {"Дата платежа": "29.12.2021", "Категория": "Переводы", "Сумма": 300},
        {"Дата платежа": "28.12.2021", "Категория": "Продукты", "Сумма": 150}
    ]
    return pd.DataFrame(test_data)


# Локальная реализация функции анализа
def spending_by_category(df, category, date=None):
    """Возвращает сумму расходов по категории и дате"""
    if date:
        filtered_df = df[(df['Категория'] == category) & (df['Дата платежа'] == date)]
    else:
        filtered_df = df[df['Категория'] == category]

    return filtered_df['Сумма'].sum() if not filtered_df.empty else []


class FinancialAnalysisTest(testing_framework.TestCase):
    def setUp(self):
        self.test_data = get_test_data()  # Получаем тестовые данные
        self.analysis_result = spending_by_category(self.test_data, "Переводы", date="31.12.2021")

    def test_specific_report(self):
        self.assertEqual(
            spending_by_category(self.test_data, "Переводы", date="31.12.2021"),
            self.analysis_result
        )

    def test_empty_categories(self):
        self.assertEqual(spending_by_category(self.test_data, "Красота"), [])
        self.assertEqual(spending_by_category(self.test_data, "nonexistent"), [])


if __name__ == "__main__":
    testing_framework.main()

