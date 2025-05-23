from fastapi import FastAPI
from app.routes.binary import router as binary_router
import uvicorn

app = FastAPI()

app.include_router(binary_router, prefix="/image")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
