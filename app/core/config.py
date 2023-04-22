from typing import Optional, Dict, Any
from pydantic import BaseSettings, validator, PostgresDsn


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    KAFKA_HOST: str
    KAFKA_PORT: int
    CURRENCY_KAFKA_TOPIC_NAME: str

    DB_URI: Optional[PostgresDsn] = None

    @validator("DB_URI", pre=True)
    def assemble_db_uri_string(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST") + f':{values.get("DB_PORT")}',
            path=f"/{values.get('DB_NAME') or ''}",
        )
    
    class Config:
        env_file = '.env'


settings = Settings()
