
# 📚 MAFIA - Middleware AI Firewall Application

**MAFIA** (Middleware AI Firewall Application) is a lightweight yet powerful Python library that integrates seamlessly into modern web frameworks to protect applications from common security threats.

> ⚠️ **Note:** MAFIA is not a replacement for enterprise-grade Web Application Firewalls (WAFs). It is designed to complement them by providing in-app protection, detection, and observability at the application layer. MAFIA is currently in early-stage research and focuses on basic yet extensible security features.

---

📦 **Features**

- ✅ AI-Powered Brute Force Attack Detection (Isolation Forest)
- ✅ Rate Limiting using Redis
- ✅ Malicious Payload Filtering (XSS & SQL Injection Patterns)
- ✅ Risk Scoring Based on Multi-Feature Input (Attempts & Interval Timing)
- ✅ Metadata Tracking & Model Versioning
- ✅ FastAPI Compatible Middleware

---

📦 **Installation**

1. Install directly from GitHub using pip:

   ```bash
   pip install git+https://github.com/akarkode/mafia.git
   ```

2. Integrate into your FastAPI project:

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

🚀 **How It Works**

1. **Incoming Request** → MAFIA logs request metadata (IP, Path)
2. **Rate Limiting** → If request count exceeds limit, request is blocked
3. **Payload Inspection** → Checks for XSS and SQLi patterns
4. **Brute Force Detection**:
   - Uses Isolation Forest trained on attempt count & interval time
   - Produces a risk score via min-max normalization
5. **Risk Decision**:
   - If risk_score > 0.8 → Request is blocked
   - Otherwise → Request is passed to the application

---

✅ **Recommended Use Cases**

- Login Endpoints
- OTP APIs
- Password Reset
- Critical Transaction Confirmations

⚠️ Not Recommended for:
- Public APIs with high traffic (e.g. product listings, open feeds)

---

📚 **References**

- Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. ICDM.
- OWASP Foundation (2021). Authentication Cheat Sheet.
- Florez et al. (2019). User Behavior Modeling. IEEE Access.
- Journal of Network and Computer Applications, Elsevier (2020).

---

🟨 **Known Limitations**

- ❌ Not suitable for high-throughput public endpoints
- ⚙️ Requires Redis for tracking state
- 📉 Accuracy depends on training data — retraining required over time
- 🔐 Does not replace strong authentication/validation logic
- 🛡️ Does **not replace a WAF**, but complements it at application level
- 🧪 Still under **active research** with focus on foundational features

---

🚧 **Planned Improvements**

- Add Geo-location & Device Fingerprint to model features
- Implement automatic retraining pipeline
- Integrate with external API Gateways (e.g. Kong, AWS)
- Real-time visualization dashboard for risk analysis

---

📧 **Contact**

For collaboration or feedback: [akarkode@gmail.com](mailto:akarkode@gmail.com)

---
