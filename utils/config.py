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

    # User-Agents for rotation (More Powerful)
    USER_AGENTS: list = field(default_factory=lambda: [
        'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.105 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
        'okhttp/4.12.0',
        'Dalvik/2.1.0 (Linux; U; Android 15; 2207117BPG Build/AP3A.240905.015.A2)',
        'Dart/3.6 (dart:io)'
    ])

    # Philippines Carrier Prefixes
    CARRIER_PREFIXES: Dict[str, str] = field(default_factory=lambda: {
        # Globe / TM
        "0905": "Globe/TM", "0906": "Globe/TM", "0915": "Globe/TM", "0916": "Globe/TM", "0917": "Globe", 
        "0926": "Globe/TM", "0927": "Globe/TM", "0935": "Globe/TM", "0936": "Globe/TM", "0937": "Globe/TM",
        "0945": "Globe/TM", "0953": "Globe/TM", "0954": "Globe/TM", "0955": "Globe/TM", "0956": "Globe/TM",
        "0965": "Globe/TM", "0966": "Globe/TM", "0967": "Globe/TM", "0975": "Globe/TM", "0976": "Globe/TM",
        "0977": "Globe/TM", "0978": "Globe/TM", "0979": "Globe/TM", "0995": "Globe/TM", "0997": "Globe/TM",
        # Smart / TNT / Sun
        "0907": "Smart/TNT", "0908": "Smart/TNT", "0909": "Smart/TNT", "0910": "Smart/TNT", "0912": "Smart/TNT",
        "0918": "Smart", "0919": "Smart", "0920": "Smart", "0921": "Smart", "0928": "Smart", "0929": "Smart",
        "0930": "Smart/TNT", "0931": "Smart/TNT", "0938": "Smart/TNT", "0939": "Smart/TNT", "0946": "Smart/TNT",
        "0947": "Smart/TNT", "0948": "Smart/TNT", "0949": "Smart/TNT", "0950": "Smart/TNT", "0951": "Smart/TNT",
        "0961": "Smart", "0963": "Smart/TNT", "0968": "Smart", "0969": "Smart", "0970": "Smart/TNT", 
        "0981": "Smart", "0989": "Smart", "0992": "Smart", "0998": "Smart", "0999": "Smart",
        "0922": "Sun", "0923": "Sun", "0924": "Sun", "0925": "Sun", "0932": "Sun", "0933": "Sun", "0934": "Sun", "0942": "Sun", "0943": "Sun",
        # DITO
        "0991": "DITO", "0992": "DITO", "0993": "DITO", "0994": "DITO", "0895": "DITO", "0896": "DITO", "0897": "DITO", "0898": "DITO",
        # GOMO
        "0976": "GOMO (Globe)",
    })

config = Config()
