import logging
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_list=".env", case_sensitive=False)

    bot_token: str
    db_url: str
    key: str
    admin: list

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
    logging.info("Configuration file loaded successfully.")
except Exception as e:
    logging.error(f"Configuration file loading error: {e}")
    exit(1)
