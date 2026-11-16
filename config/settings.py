import os
from typing import Dict, Any

class Settings:
    """Centralized configuration for UI and API tests."""
    
    # UI Configuration (SauceDemo)
    UI_BASE_URL: str = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
    
    # Standard SauceDemo Test Users
    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_OUT_USER: str = os.getenv("LOCKED_OUT_USER", "locked_out_user")
    PROBLEM_USER: str = os.getenv("PROBLEM_USER", "problem_user")
    PERFORMANCE_GLITCH_USER: str = os.getenv("PERFORMANCE_GLITCH_USER", "performance_glitch_user")
    STANDARD_PASSWORD: str = os.getenv("STANDARD_PASSWORD", "secret_sauce")
    
    # API Configuration (ReqRes public REST API)
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://reqres.in")
    
    # Browser & Execution Settings
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "10000"))  # milliseconds
    
    # Viewports / Devices
    DESKTOP_VIEWPORT: Dict[str, int] = {"width": 1920, "height": 1080}
    MOBILE_DEVICE_NAME: str = os.getenv("MOBILE_DEVICE_NAME", "Pixel 5")
    
    # Test Data Defaults
    CUSTOMER_FIRST_NAME: str = "John"
    CUSTOMER_LAST_NAME: str = "Doe"
    CUSTOMER_POSTAL_CODE: str = "94043"

settings = Settings()
