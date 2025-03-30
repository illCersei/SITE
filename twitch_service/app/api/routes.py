from fastapi import APIRouter
import json
from fastapi_cache import FastAPICache

router = APIRouter()

@router.get("/api/games")
async def get_games():
    """Возвращает список игр из кэша, если есть"""
    cache_backend = FastAPICache.get_backend()
    cached_games = await cache_backend.get("cached_games")

    if cached_games:
        return json.loads(cached_games)  
    return [] 

@router.get("/api/viewers")
async def get_viewers():
    """Возвращает данные о зрителях из кэша Redis"""
    cache_backend = FastAPICache.get_backend()
    cached_viewers = await cache_backend.get("cached_viewers")

    if cached_viewers:
        return json.loads(cached_viewers)  
    return []
