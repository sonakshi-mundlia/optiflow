from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "OptiFlow"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str
    REDIS_URL: str
    GEMINI_API_KEY: str

    SEMANTIC_CACHE_THRESHOLD: float 

    MAX_CACHE_ENTRIES: int 

    MAX_CONCURRENT_INFERENCE: int 


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()