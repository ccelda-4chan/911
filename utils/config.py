import os
from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class Config:
    APP_PASSWORD: str = os.environ.get("APP_PASSWORD", "admin")
    SESSION_SECRET: str = os.environ.get("SESSION_SECRET", "super-secret-key-change-me")
    MAX_CONCURRENT_ATTACKS: int = int(os.environ.get("MAX_CONCURRENT_ATTACKS", "10"))
    RENDER: bool = os.environ.get("RENDER", "False").lower() == "true"
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    
    # Service specific magic values/keys
    FINGERPRINT_VISITOR_ID: str = "TPt0yCuOFim3N3rzvrL1"
    FINGERPRINT_REQUEST_ID: str = "1757149666261.Rr1VvG"
    KOMO_SIGNATURE: str = "ET/C2QyGZtmcDK60Jcavw2U+rhHtiO/HpUTT4clTiISFTIshiM58ODeZwiLWqUFo51Nr5rVQjNl6Vstr82a8PA=="
    KOMO_SUBSCRIPTION_KEY: str = "cfde6d29634f44d3b81053ffc6298cba"

config = Config()
