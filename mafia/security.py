import re

class SecurityFilter:
    def __init__(self):
        self.xss_pattern = re.compile(r"(<script>|<.*onerror=.*?>)", re.IGNORECASE)
        self.sqli_pattern = re.compile(r"(UNION|SELECT|DROP|INSERT|UPDATE|DELETE|--|\")", re.IGNORECASE)

    def is_malicious(self, payload: str) -> bool:
        return bool(self.xss_pattern.search(payload) or self.sqli_pattern.search(payload))
