from fastapi import FastAPI
import uvicorn
from app.routes.auth_routes import router as auth_router


app = FastAPI()


app.include_router(auth_router, prefix="/auth")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)