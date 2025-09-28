import os

class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./hssdi.db")
    secret_key: str = "hssdi-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    admin_username: str = "admin"
    admin_password: str = "admin123"

    # Redis settings for session management
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

settings = Settings()