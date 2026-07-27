from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sql_server: str
    sql_database: str
    sql_user: str
    sql_password: str
    sql_driver: str
    sql_schema: str
    #sql_pool_size: int

    gemini_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()