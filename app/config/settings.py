
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sql_server: str
    sql_database: str
    sql_user: str
    sql_password: str
    sql_driver: str
    sql_schema: str
    #sql_pool_size: int

# Azure OpenAI
    azure_openai_api_endpoint: str
    azure_openai_api_deployment_name: str
    azure_openai_api_key: str
    azure_openai_api_version: str


    class Config:
        env_file = ".env"


settings = Settings()