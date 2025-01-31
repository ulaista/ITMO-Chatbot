import time
from typing import List, Optional
import openai
import requests
import os
import feedparser  # RSS-парсинг новостей

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, HttpUrl
from utils.logger import setup_logger

# Инициализация FastAPI
app = FastAPI()
logger = None

# API-ключи
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # GPT API Key
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")  # API-ключ Google
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  # Google Search ID

# Инициализация OpenAI Client (НОВЫЙ СИНТАКСИС)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Модели запросов и ответов
class PredictionRequest(BaseModel):
    query: str
    id: int

class PredictionResponse(BaseModel):
    id: int
    answer: Optional[int]
    reasoning: str
    sources: List[HttpUrl]

@app.on_event("startup")
async def startup_event():
    global logger
    logger = await setup_logger()

# Функция обработки запроса через GPT
def get_model_response(query):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Ты помощник, отвечающий на вопросы об Университете ИТМО."},
                      {"role": "user", "content": query}]
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        print(f"Ошибка OpenAI API: {e}")
        return "Ошибка при обращении к OpenAI API"

# Функция поиска ссылок в интернете
def search_links(query):
    try:
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": SEARCH_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "num": 3
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if "items" in data:
            return [item["link"] for item in data["items"]]
        else:
            return []
    except requests.RequestException as e:
        print(f"Ошибка поиска Google API: {e}")
        return []

# Функция получения новостей ИТМО
def get_latest_news():
    try:
        feed = feedparser.parse("https://itmo.ru/rss")
        return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:3]]
    except Exception as e:
        print(f"Ошибка при получении новостей: {e}")
        return []

@app.post("/api/request", response_model=PredictionResponse)
async def predict(body: PredictionRequest):
    try:
        await logger.info(f"Processing request: {body.id}")
        
        response_text = get_model_response(body.query)
        sources = search_links(body.query)

        # Определение правильного ответа
        answer = None
        if any(str(i) + "." in body.query for i in range(1, 11)):
            for i in range(1, 11):
                if f"{i}." in body.query and str(i) in response_text:
                    answer = i
                    break
        
        response = PredictionResponse(
            id=body.id,
            answer=answer,
            reasoning=response_text,
            sources=sources,
        )
        await logger.info(f"Successfully processed request {body.id}")
        return response
    except Exception as e:
        await logger.error(f"Error processing request {body.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/news")
async def get_news():
    return {"news": get_latest_news()}
