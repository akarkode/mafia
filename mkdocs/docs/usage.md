
🚀 Usage Instructions

✅ Integrate with FastAPI

    from fastapi import FastAPI
    from mafia.middleware import BruteForceMiddleware

    app = FastAPI()
    app.add_middleware(BruteForceMiddleware, redis_url="redis://localhost:6379")

    @app.get("/")
    def home():
        return {"message": "Hello from MAFIA-protected API!"}

📌 Recommended Use Cases

- Login Endpoints
- OTP Sending APIs
- Password Reset
- Transaction Verification

⚠️ Not Recommended for High-Traffic APIs like Product Listing or Public Data APIs.