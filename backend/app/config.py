from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "XAUUSD Terminal"
    ENVIRONMENT: str = "development"

    OANDA_API_KEY: str = ""
    OANDA_ACCOUNT_ID: str = ""
    OANDA_BASE_URL: str = "https://api-fxpractice.oanda.com"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    class Config:
        env_file = ".env"

settings = Settings()
