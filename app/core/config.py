from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    TOP_K_RESULTS: int = 3
    SIMILARITY_THRESHOLD: float = 0.4

    class Config:
        env_file = ".env"
        extra = "ignore" 


settings = Settings()