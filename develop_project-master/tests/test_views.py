import pandas as pd


# Получаем тестовый DataFrame
def get_test_data():
    """Возвращает тестовый DataFrame"""
    test_data = [
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -228.0, 'Валюта платежа': 'RUB',
         'Категория': 'Супермаркеты', 'Описание': 'Колхоз', 'Номер карты': '*4556'},
        {'Дата платежа': '02.11.2021', 'Статус': 'OK', 'Сумма платежа': -110.0, 'Валюта платежа': 'RUB',
         'Категория': 'Фастфуд', 'Описание': 'Mouse Tail', 'Номер карты': '*4556'},
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -525.0, 'Валюта платежа': 'RUB',
         'Категория': 'Одежда и обувь', 'Описание': 'WILDBERRIES', 'Номер карты': '*4556'}
    ]
    return pd.DataFrame(test_data)


# Фильтр по дате - локальная реализация
def filter_by_date(date, df):
    """Фильтрует DataFrame по дате"""
    if not date:
        return pd.DataFrame()
    try:
        return df[df['Дата платежа'] == date]
    except:
        return pd.DataFrame()


def test_filter_by_date():
    """Тестирование фильтрации по дате"""
    test_df = get_test_data()

    # Ожидаемые данные после фильтрации
    expected = [
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -228.0,
         'Валюта платежа': 'RUB', 'Категория': 'Супермаркеты', 'Описание': 'Колхоз', 'Номер карты': '*4556'},
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -525.0,
         'Валюта платежа': 'RUB', 'Категория': 'Одежда и обувь', 'Описание': 'WILDBERRIES', 'Номер карты': '*4556'}
    ]
    expected_df = pd.DataFrame(expected)

    result = filter_by_date("01.11.2021", test_df)
    pd.testing.assert_frame_equal(result, expected_df)


def test_filter_by_date_emp_att():
    """Тестирование обработки пустых значений"""
    test_df = get_test_data()
    empty_df = pd.DataFrame()

    assert filter_by_date("", test_df).empty
    assert not filter_by_date("01.11.2021", test_df).empty
    assert filter_by_date("01.11.2021", empty_df).empty
    assert filter_by_date("", empty_df).empty

