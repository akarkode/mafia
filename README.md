# 📚 MAFIA - Middleware AI Firewall Application

MAFIA (Middleware AI Firewall Application) is a lightweight yet powerful Python library that integrates seamlessly into modern web frameworks to protect applications from common security threats.

📦 Features

- AI-Powered Brute Force Attack Detection (Isolation Forest)
- Rate Limiting using Redis
- Malicious Payload Filtering (XSS & SQL Injection Patterns)
- Risk Scoring Based on Multi-Feature Input (Attempts & Interval Timing)
- Metadata Tracking & Model Versioning
- FastAPI Compatible Middleware

---

📚 Installation

1. Install Directly from GitHub using Pip

   ```bash
   pip install git+https://github.com/akarkode/mafia.git
   ```
   
2. Integrate into FastAPI Project
   ```python
   from fastapi import FastAPI
   from mafia.middleware import BruteForceMiddleware

   app = FastAPI()
   app.add_middleware(BruteForceMiddleware, redis_url="redis://localhost:6379")

   @app.get("/")
   def home():
   return {"message": "Hello from MAFIA-protected API!"}
   ```

---

🚀 How It Works

1. Incoming Request → MAFIA logs request metadata (IP, Path).
2. Rate Limiting → If request count exceeds limit, request is blocked.
3. Payload Inspection → Checks for malicious patterns in query parameters (XSS, SQL Injection).
4. Brute Force Detection (AI) →
   - Uses Isolation Forest trained on attempt_count and avg_interval_between_attempts.
   - Produces a risk score using min-max normalization.
5. Risk Decision →
   - If risk_score > 0.8, request is blocked.
   - Otherwise, request proceeds to application logic.

---

📚 References

- Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. In IEEE International Conference on Data Mining (ICDM).
- OWASP Foundation. (2021). Authentication Cheat Sheet.
- Florez et al., (2019). User Behavior Modeling in Authentication Systems. IEEE Access.
- Journal of Network and Computer Applications, Elsevier (2020).

---

✅ Recommended Use Cases

- Login Endpoints
- OTP Sending / Verification APIs
- Password Reset APIs
- Critical Transaction Confirmation APIs

⚠️ Not Recommended for High-Frequency Public APIs (e.g., Product Listings, Public Feeds)

---

📚 Advantages

- AI-Driven Detection (Adapts to new attack patterns)
- Lightweight and Easy to Integrate
- Centralized Logging and Risk Scoring
- Easy Monitoring and Extendable

---

⚠️ Limitations

- Not Suitable for High-Throughput APIs
- Requires Redis for State Management
- Needs Periodic Model Retraining for Optimal Accuracy
- Not a Replacement for Proper Authentication & Validation Layers

---

📅 Future Improvements

- Add Advanced Behavioral Features (Geo-Location, Device Fingerprint)
- Self-Learning Retraining Pipeline
- Integration with API Gateways (Kong, AWS API Gateway)
- Real-time Visualization Dashboard

---

📧 Contact

For more information or collaboration, contact: akarkode@gmail.com
