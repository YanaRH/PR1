import os
import configparser
from pathlib import Path


class EnvConfig:
    def __init__(self):
        self.env_file = Path('.env')
        self.config = configparser.ConfigParser()
        self._load_env()
        self._load_config()

    def _load_env(self):
        """Загружает переменные окружения из .env файла"""
        if not self.env_file.exists():
            print(f"Файл {self.env_file} не найден!")
            return

        with open(self.env_file) as f:
            for line in f:
                line = line.strip()
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue

                # Разделяем переменные (учитываем по первому знаку =)
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Удаляем кавычки если они есть
                    if (value.startswith('"') and value.endswith('"')) or \
                            (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    os.environ[key] = value
                except ValueError as e:
                    print(f"Ошибка в строке .env: {line}")

    def _load_config(self):
        """Загружает конфигурацию из config.ini"""
        config_file = Path('config.ini')
        if config_file.exists():
            self.config.read(config_file)

    def get(self, key, default=None):
        """Получает значение из переменных окружения или конфига"""
        return os.getenv(key) or self.config.get('DEFAULT', key, fallback=default)


# Пример использования
if __name__ == "__main__":
    env = EnvConfig()

    # Доступ к переменным окружения
    print("Database Host:", env.get("DB_HOST"))
    print("API Key:", env.get("API_KEY"))
    print("App Environment:", env.get("APP_ENV"))

    # Проверка существования ключа
    missing_key = env.get("NON_EXISTENT_KEY")
    if missing_key is None:
        print("Ключ не найден")












