# ITMO Chatbot

## 📌 Описание
**ITMO Chatbot** — это REST API сервис, предоставляющий информацию об Университете ИТМО. Бот использует **GPT**, **поиск по интернету (Google Custom Search API)** и **RSS-новости** для формирования ответов.

---
## 🚀 Функциональность
- 📖 Отвечает на вопросы о **направлениях, факультетах, рейтингах, истории** ИТМО.
- 🔎 Выполняет **поиск в интернете** для актуальных данных.
- 📰 Получает **последние новости** через RSS ITMO.
- 🛠 Поддержка **Docker** и **REST API**.

---
## ⚙️ Технологии
- **FastAPI** — серверное приложение
- **OpenAI GPT API** — генерация ответов
- **Google Custom Search API** — поиск источников
- **RSS ITMO** — последние новости
- **Docker, Docker Compose** — контейнеризация

---
## 📌 Установка и запуск

### 1️⃣ 🔑 **Создание API-ключей**
Перед запуском необходимо получить API-ключи:
- **OpenAI API Key** (для GPT-4)
- **Google Custom Search API Key** (поиск по ИТМО)
- **Google Search Engine ID** (поисковый идентификатор)

### 2️⃣ 🛠 **Создать `.env` файл**
Создайте файл `.env` в корне проекта и добавьте:
```ini
OPENAI_API_KEY=your_openai_key
SEARCH_API_KEY=your_google_search_key
SEARCH_ENGINE_ID=your_search_engine_id
```

### 3️⃣ 🐳 **Запуск через Docker**
```sh
docker-compose up -d --build
```

### 4️⃣ 📡 **Проверка работы API**
#### ✅ Проверка состояния сервиса
```sh
curl http://localhost:8080/docs
```
#### ✅ Получение ответа на запрос
```sh
curl --location --request POST 'http://localhost:8080/api/request' \
--header 'Content-Type: application/json' \
--data-raw '{
  "query": "Какие направления есть в Университете ИТМО?",
  "id": 1
}'
```
Пример ответа:
```json
{
  "id": 1,
  "answer": null,
  "reasoning": "ИТМО предлагает широкий спектр направлений...",
  "sources": ["https://itmo.ru/", "https://student.itmo.ru/"]
}
```
#### ✅ Получение новостей
```sh
curl http://localhost:8080/api/news
```
Пример ответа:
```json
{
  "news": [
    {"title": "ИТМО вошел в топ-100 мировых университетов", "link": "https://news.itmo.ru/news_1"},
    {"title": "Новая AI-лаборатория в ИТМО", "link": "https://news.itmo.ru/news_2"}
  ]
}
```

---
## 📌 **Структура проекта**
```
├── app/
│   ├── main.py          # Основной сервер FastAPI
│   ├── config.py        # Настройки API
│   ├── utils.py         # Вспомогательные функции
│   └── logger.py        # Логирование
├── Dockerfile           # Сборка контейнера
├── docker-compose.yml   # Конфигурация сервисов
├── requirements.txt     # Зависимости
└── README.md            # Описание проекта
```

---
## 📌 Развертывание в облаке
Можно развернуть сервис на:
- ☁️ **Heroku**
- ☁️ **Yandex Cloud**
- ☁️ **AWS / GCP**

Пример команды для Heroku:
```sh
git push heroku main
```

---
## 🛠 **Дополнительные настройки**

### 🔍 **Изменение логов**
Логи хранятся в папке `logs/` внутри контейнера. Чтобы посмотреть их:
```sh
docker logs itmo-chatbot
```

### 🔄 **Перезапуск сервиса**
```sh
docker-compose restart
```

### 🛑 **Остановка контейнера**
```sh
docker-compose down
```
