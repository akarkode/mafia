
# MAFIA - Middleware AI Firewall Application

**MAFIA** is a Python middleware designed to detect and prevent brute force attacks and block malicious payloads (such as XSS, SQL Injection, etc.). This middleware can be easily integrated into FastAPI or Starlette-based applications.

---

## 🔧 Instalation

```bash
pip install git+https://github.com/akarkode/mafia.git
```

---

## 🚀 Usage

Add the middleware to your FastAPI application:
```python
from mafia.middleware import BruteForceMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(BruteForceMiddleware, redis_url="redis://localhost:6379")
```

This middleware will automatically:
- Detect and block suspicious requests from the same IP.
- Classify login attempts using an AI-based model.
- Block any requests containing potentially malicious payloads.

---

## 🛡️ Security Features

### 1. Brute Force Detection
The `BruteForceDetector` AI model analyzes login attempt patterns based on frequency and interval features.

### 2. Malicious Payload Filtering
The `SecurityFilter` scans and blocks:
- XSS attacks: `<script>`, `onerror=`, `javascript:`
- SQL Injection: `' OR 1=1`, `UNION SELECT`, `--`, etc.

### 3. Rate Limiting
The `RedisClient` module limits request frequency based on the user's IP address.

---

## 🧠 Internal Architecture

```text
[Client] → [BruteForceMiddleware]
   ├─ [RedisClient] - rate limiting
   ├─ [BruteForceDetector] - brute force classification
   └─ [SecurityFilter] - XSS/SQLi filtering
```

### Key Classes and Functions
- `BruteForceMiddleware`
  - `dispatch()`: Core middleware process
- `BruteForceDetector`
  - `predict(features: list) -> bool`
  - `train()`, `save_model()`
- `SecurityFilter`
  - `is_malicious(payload: str) -> bool`

---

## 📈 Future Improvements

- Real-time log visualization dashboard.
- Integration with ElasticSearch for advanced logging.
- LSTM-based AI model for more accurate login pattern recognition.
- Periodic automatic training of the detection model.

---

## 📄 License and Contribution

Please refer to the `LICENSE` file for license details. Pull requests, issues, and contributions are very welcome.

---

> This documentation is built using MkDocs Material as a single page for simplicity and fast access.
