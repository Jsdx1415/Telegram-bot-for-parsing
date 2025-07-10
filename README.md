# Telegram Bot for Parsing

Автоматизированный бот на базе aiogram, Playwright и PostgreSQL для периодического парсинга данных и отправки их в Telegram.

## Описание

Бот позволяет:

- Автоматически регистрировать пользователя при первом запуске бота с хранением логина и зашифрованного пароля; для смены данных используйте команду `/relogin`.
- Периодически (настраиваемый интервал) выполнять парсинг целевых данных через Playwright и отправлять обновления пользователю.
- Управлять расписанием задач с помощью APScheduler.
- Обрабатывать команды и ввод пользователя асинхронно.

## Требования

- Python 3.11+
- PostgreSQL 12+
- Docker (рекомендуется)

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Jsdx1415/Telegram-bot-for-parsing.git
   cd Telegram-bot-for-parsing
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate  # Windows
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## Конфигурация

Создайте файл `.env` в корне проекта по примеру `.env.example`:

```
BOT_TOKEN=ваш_токен_бота
DB_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
KEY=секретный_ключ_для_шифрования
ADMIN=[123456789]
```

## Развёртывание PostgreSQL в Docker Desktop

Чтобы развернуть PostgreSQL без файлов Compose, воспользуйтесь графическим интерфейсом Docker Desktop:

1. Откройте **Docker Desktop**.
2. Перейдите на вкладку **Images** и нажмите **Pull**. Введите образ:
   ```text
   postgres:13
   ```
3. После скачивания перейдите в **Containers / Apps** и нажмите **Run** напротив образа `postgres:13`.
4. В окне запуска задайте параметры:
   - **Container Name**: `telegram-postgres`
   - **Image**: `postgres:13`
   - **Environment Variables**:
     - `POSTGRES_USER` = `<your_username>`
     - `POSTGRES_PASSWORD` = `<your_password>`
     - `POSTGRES_DB` = `<your_database>`
   - **Port mapping**: `5432` → `5432`
   - **Volumes**: создайте новый volume `telegram-postgres-data`, смонтируйте в `/var/lib/postgresql/data`
5. Нажмите **Run**. Контейнер запустится и будет доступен по адресу `localhost:5432`.

В файле `.env` вашего бота укажите параметры подключения:

```env
DB_URL=postgresql+asyncpg://<your_username>:<your_password>@localhost:5432/<your_database>
```

## Запуск

### Локально

```bash
python main.py
```

## Структура проекта

```plain
├── main.py                # Точка входа: инициализация бота и шедулера
├── config/                # Pydantic Settings, конфигурация
├── app/
│   ├── handlers/          # Роутеры команд (registration, parser и др.)
│   ├── database/          # Модели и функции работы с базой данных
│   └── parser/            # Логика Playwright-парсера(нужно написать самому для ваших целей)
├── requirements.txt       # Зависимости проекта
├── .env.example           # Пример файла окружения
└── README.md              # Этот файл
```

## Команды бота

- `/start` — запуск бота, автоматическая регистрация и приветствие
- `/relogin` — смена логина и пароля
- `/parser` — тестовый (неплановый) запуск парсера

## Конфигурация парсинга

Частота запуска задач задаётся в `app/parser/main_parser.py` через APScheduler. По умолчанию парсинг происходит каждый час.

## Лицензия

Проект распространяется под лицензией MIT.

---

Если возникнут вопросы или предложения — открывайте issue или присылайте PR!
