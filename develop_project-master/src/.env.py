import pandas as pd


# Функция для фильтрации транзакций по параметрам
def filter_transactions(df: pd.DataFrame,
                        start_date: str = None,
                        end_date: str = None,
                        category: str = None,
                        min_amount: float = None) -> pd.DataFrame:
    """
    Полная фильтрация транзакций по заданным параметрам
    :param df: DataFrame с транзакциями
    :param start_date: Начальная дата периода (формат 'YYYY-MM-DD')
    :param end_date: Конечная дата периода (формат 'YYYY-MM-DD')
    :param category: Категория транзакций
    :param min_amount: Минимальная сумма транзакции
    :return: Отфильтрованный DataFrame
    """
    # Проверяем что передан DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Должен быть передан pandas.DataFrame")

    # Если DataFrame пустой, возвращаем его
    if df.empty:
        return df

    # Фильтруем по датам, если они указаны
    if start_date or end_date:
        try:
            if start_date:
                start_date = pd.to_datetime(start_date)
                df = df[df['Дата платежа'] >= start_date]
            if end_date:
                end_date = pd.to_datetime(end_date)
                df = df[df['Дата платежа'] <= end_date]
        except Exception as e:
            raise ValueError(f"Ошибка обработки дат: {e}")

    # Фильтруем по категории, если указана
    if category:
        df = df[df['Категория'] == category]

    # Фильтруем по минимальной сумме, если указана
    if min_amount is not None:
        df = df[df['Сумма платежа'] >= min_amount]

    return df


def main():
    """Пример использования функции"""
    # Тестовые данные
    data = {
        'Дата платежа': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Сумма платежа': [100, 200, 150]
    }
    df = pd.DataFrame(data)

    # Фильтрация
    try:
        filtered = filter_transactions(df,
                                       start_date='2023-01-02',
                                       category='Еда')
        print(filtered)
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()











