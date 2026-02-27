from fastapi import FastAPI, Request
from mafia.middleware import BruteForceMiddleware

app = FastAPI(title="MAFIA Protected API", version="0.1.0")
app.add_middleware(BruteForceMiddleware, redis_url="redis://localhost:6379")


@app.get("/")
def home():
    return {"message": "Hello from MAFIA-protected API!"}


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    return {"message": "Login received", "user": body.get("username")}


@app.post("/otp")
async def verify_otp(request: Request):
    body = await request.json()
    return {"message": "OTP received", "otp": body.get("otp")}
