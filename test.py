import asyncio
import aiohttp
import time
import random

# Тестируемый эндпоинт
API_URL = "http://localhost:8080/api/request"

# Список тестовых вопросов
test_queries = [
    "В каком году был основан Университет ИТМО?\n1. 1900\n2. 1905\n3. 1910\n4. 1920",
    "Какой цвет является основным в фирменном стиле Университета ИТМО?\n1. Красный\n2. Синий\n3. Зелёный\n4. Жёлтый",
    "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Новосибирск\n4. Казань",
    "Какой рейтинг впервые включил ИТМО в топ-400 мировых университетов?\n1. QS\n2. THE\n3. ARWU\n4. U.S. News",
    "Какое направление активно развивается в ИТМО?\n1. Искусственный интеллект\n2. Дизайн\n3. Биоинженерия\n4. Робототехника",
]

NUM_REQUESTS = 100  # Общее число запросов
CONCURRENT_REQUESTS = 10  # Одновременно выполняемых запросов

async def send_request(session, query, req_id):
    """Отправка запроса и замер времени"""
    payload = {"query": query, "id": req_id}
    start_time = time.time()

    try:
        async with session.post(API_URL, json=payload, ssl=False) as response:
            response_json = await response.json()
            response_time = time.time() - start_time
            return response.status, response_time, response_json
    except Exception as e:
        return None, None, str(e)

async def stress_test():
    """Запуск стресс-теста"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(NUM_REQUESTS):
            query = random.choice(test_queries)
            tasks.append(send_request(session, query, i + 1))

            # Ограничение на количество одновременных запросов
            if len(tasks) >= CONCURRENT_REQUESTS:
                results = await asyncio.gather(*tasks)
                for status, response_time, response_json in results:
                    if status == 200:
                        print(f"✅ Запрос {response_json['id']} выполнен за {response_time:.2f} сек")
                    else:
                        print(f"❌ Ошибка в запросе {response_json}: {status}")
                tasks = []  # Очистка списка задач перед следующим пакетом

        # Выполнение оставшихся задач
        if tasks:
            results = await asyncio.gather(*tasks)
            for status, response_time, response_json in results:
                if status == 200:
                    print(f"✅ Запрос {response_json['id']} выполнен за {response_time:.2f} сек")
                else:
                    print(f"❌ Ошибка в запросе {response_json}: {status}")

# Исправленный запуск
if __name__ == "__main__":
    asyncio.run(stress_test())
