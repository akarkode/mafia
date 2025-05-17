from fastapi import FastAPI
from mafia.middleware import BruteForceMiddleware

app = FastAPI()
app.add_middleware(BruteForceMiddleware, redis_url="redis://localhost:6379")

@app.get("/")
def home():
    return {"message": "Hello from MAFIA-protected app!"}
