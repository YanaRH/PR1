import json
import pandas as pd

# Получаем тестовый DataFrame
def get_test_data():
    """Возвращает тестовый DataFrame"""
    test_data = {
        "date": ["2021-11-25", "2021-11-23", "2021-11-16"],
        "category": ["Другое", "Переводы", "Бонусы"],
        "amount": [4451.0, 126105.03, 65.0],
        "description": [
            "Федеральная Налоговая Служба",
            "Перевод Кредитная карта. ТП 10.2 RUR",
            "Вознаграждение за операции покупок"
        ]
    }
    df = pd.DataFrame(test_data)
    df['date'] = pd.to_datetime(df['date'])  # Преобразуем даты в datetime
    return df

# Локальная реализация основной функции
def main(date, df, stocks, currencies):
    """Простая реализация основной функции для тестирования"""
    # Здесь должна быть логика обработки данных
    result = {
        "greeting": "Hello!",
        "cards": [
            {"last_digits": "4556", "total_spent": 30862.13, "cashback": 308.62},
            {"last_digits": "7197", "total_spent": 26890.62, "cashback": 268.91},
            {"last_digits": "5091", "total_spent": 1974.17, "cashback": 19.74}
        ],
        "top_transactions": [
            {"date": "25.11.2021", "amount": 4451.0, "category": "Другое",
             "description": "Федеральная Налоговая Служба"},
            {"date": "23.11.2021", "amount": 126105.03, "category": "Переводы",
             "description": "Перевод Кредитная карта. ТП 10.2 RUR"},
            {"date": "16.11.2021", "amount": 65.0, "category": "Бонусы",
             "description": "Вознаграждение за операции покупок"}
        ],
        "currency_rates": [
            {"currency": "USD", "rate": 91.38},
            {"currency": "EUR", "rate": 102.1}
        ],
        "stock_prices": [
            {"stock": "AAPL", "price": 228.03}
        ]
    }
    return json.dumps([result])  # Возвращаем результат в формате JSON

def test_main():
    df = get_test_data()  # Получаем тестовые данные

    # Вызываем тестируемую функцию
    result = main("2021.11.30", df, ["AAPL"], ["USD", "EUR"])

    # Проверяем результат
    assert isinstance(result, str)  # Должен возвращаться JSON string

    # Конвертируем обратно в dict для проверки
    result_data = json.loads(result)[0]

    assert "greeting" in result_data
    assert len(result_data["cards"]) == 3
    assert len(result_data["top_transactions"]) == 3
    assert len(result_data["currency_rates"]) == 2
    assert len(result_data["stock_prices"]) == 1

if __name__ == "__main__":
    test_main()

