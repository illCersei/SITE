import asyncio
import json
from fastapi_cache import FastAPICache
from app.bd.database import AsyncSessionLocal
from sqlalchemy.sql import text  

async def fetch_games_from_db(db):
    """Запрос списка игр из БД"""
    result = await db.execute(text("SELECT game_id, game_name FROM games")) 
    return [dict(row) for row in result.mappings().all()]

async def fetch_viewers_from_db(db):
    """Запрос количества зрителей из БД"""
    result = await db.execute(
        text("SELECT SUM(viewers) AS total_viewers, TO_CHAR(date_time, 'YYYY-MM-DD HH24:MI') AS date FROM viewer GROUP BY date ORDER BY date")
    )  
    return [dict(row) for row in result.mappings().all()]

async def update_cache():
    """Фоновая задача обновления кэша каждые 5 минут"""
    while True:
        print("[INFO] Обновление кэша...")

        async with AsyncSessionLocal() as db:
            games = await fetch_games_from_db(db)
            viewers = await fetch_viewers_from_db(db)

            games_json = json.dumps(games)
            viewers_json = json.dumps(viewers)

            cache_backend = FastAPICache.get_backend()

            await cache_backend.clear("cached_games")
            await cache_backend.clear("cached_viewers")

            await cache_backend.set("cached_games", games_json, expire=300)
            await cache_backend.set("cached_viewers", viewers_json, expire=300)

        print("[INFO] Кэш обновлён!")
        await asyncio.sleep(120)  
