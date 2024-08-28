import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./test.db"
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    STATIC_DIR: str = os.path.join(PROJECT_ROOT, "static")
    TEMPLATE_DIR: str = os.path.join(PROJECT_ROOT, "templates")
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_ORDERS_TOPIC: str = "new_orders"

    class Config:
        env_file = ".env"


settings = Settings()