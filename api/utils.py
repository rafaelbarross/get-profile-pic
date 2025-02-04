import random
from typing import Optional

def get_random_proxy() -> Optional[str]:
    """
    You can add a list of proxy servers here if needed.
    Format: protocol://user:pass@ip:port
    """
    proxy_list = [
        # Add your proxy servers here if needed
        # "http://proxy1.example.com:8080",
        # "http://proxy2.example.com:8080",
    ]
    
    return random.choice(proxy_list) if proxy_list else None
