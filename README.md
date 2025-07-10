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

## Configuration

Create a `.env` file in the project root based on `.env.example`:

```
BOT_TOKEN=<your_bot_token>
DB_URL=postgresql+asyncpg://<your_username>:<your_password>@localhost:5432/<your_database>
KEY=<your_encryption_key>
ADMIN=[123456789]
```

## Развёртывание PostgreSQL с помощью Docker CLI

Чтобы быстро запустить PostgreSQL через Docker в командной строке, выполните следующие шаги:

1. **Загрузка образа**:
   ```bash
   docker pull postgres
   ```
2. **Запуск контейнера**:
   ```bash
   docker run -d \
     --name telegram-postgres \
     -e POSTGRES_USER=<ваш_пользователь> \
     -e POSTGRES_PASSWORD=<ваш_пароль> \
     -e POSTGRES_DB=<ваша_база> \
     -p 5432:5432 \
     -v telegram-postgres-data:/var/lib/postgresql/data \
     postgres
   ```
3. **Проверка статуса**:
   ```bash
   docker ps
   ```
4. **Подключение из бота**

   В файле `.env` вашего бота укажите:
   ```env
   DB_URL=postgresql+asyncpg://<your_username>:<your_password>@localhost:5432/<your_database>
   ```

---

## Дополнительный вариант: Развёртывание PostgreSQL в Docker Desktop

Чтобы развернуть PostgreSQL без файлов Compose, воспользуйтесь графическим интерфейсом Docker Desktop:

1. Откройте **Docker Desktop**.
2. Перейдите на вкладку **Images** и нажмите **Pull**. Введите образ:
   ```text
   postgres
   ```
3. После скачивания перейдите в **Containers / Apps** и нажмите **Run** напротив образа `postgres`.
4. В окне запуска задайте параметры:
   - **Container Name**: `telegram-postgres`
   - **Image**: `postgres`
   - **Environment Variables**:
     - `POSTGRES_USER` = `<your_username>`
     - `POSTGRES_PASSWORD` = `<your_password>`
     - `POSTGRES_DB` = `<your_database>`
   - **Port mapping**: `5432` → `5432`
   - **Volumes**: создайте новый volume `telegram-postgres-data`, смонтируйте в `/var/lib/postgresql/data`
5. Нажмите **Run**. Контейнер запустится и будет доступен по адресу `localhost:5432`.

В файле `.env` вашего бота укажите те же параметры подключения:

```env
DB_URL=postgresql+asyncpg://<your_username>:<your_password>@localhost:5432/<your_database>
```

## Запуск

### Локально

```bash
python main.py
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

