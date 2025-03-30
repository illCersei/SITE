from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.api.update_cache import update_cache
import uvicorn
import asyncio
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Инициализация Redis и запуск фоновой задачи обновления кэша """
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    asyncio.create_task(update_cache())  
    yield  

    
app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
