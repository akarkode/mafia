📈 System Architecture

🔥 How MAFIA Works

1. Incoming Request → Logs metadata (IP, Path).
2. Rate Limiting → If request exceeds threshold, it’s blocked.
3. Payload Filtering → Detects XSS & SQLi patterns.
4. Brute Force Detection → 
    - Uses Isolation Forest trained on attempt_count and avg_interval_between_attempts.
    - Calculates normalized risk score.
5. Decision → If risk_score > 0.8, request is blocked.