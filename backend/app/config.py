from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "123456"
    db_name: str = "diabetes_manage_db"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    ai_api_base: str = "https://yunying.jieyisoft.com:30170"
    ai_chat_path: str = "/v1/chat/completions"
    ai_api_key: str = ""
    ai_model: str = "deepseek-v4-pro"
    ai_timeout_seconds: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        )

    @property
    def ai_chat_url(self) -> str:
        return f"{self.ai_api_base.rstrip('/')}/{self.ai_chat_path.lstrip('/')}"


settings = Settings()
