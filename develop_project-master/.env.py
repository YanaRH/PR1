import os

# Настройка переменных окружения
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "your_database_name"
os.environ["DB_USER"] = "your_database_user"
os.environ["DB_PASSWORD"] = "your_database_password"
os.environ["API_KEY"] = "your_api_key"
os.environ["API_SECRET"] = "your_api_secret"
os.environ["API_URL"] = "https://api.example.com"
os.environ["APP_ENV"] = "development"  # или production
os.environ["APP_DEBUG"] = "True"  # или False
os.environ["APP_PORT"] = "8000"
os.environ["LOG_LEVEL"] = "INFO"

# Пример доступа к переменным окружения
if __name__ == "__main__":
    print("Database Host:", os.getenv("DB_HOST"))
    print("API Key:", os.getenv("API_KEY"))
    print("App Environment:", os.getenv("APP_ENV"))










