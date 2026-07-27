# ======================
# IMPORTS
# ======================
from functools import lru_cache
 
from langchain_openai import AzureChatOpenAI
 
from app.config.settings import settings
 
 
def openai_enabled() -> bool:
    return settings.openai_enabled
 
 
@lru_cache(maxsize=1)
def get_llm() -> AzureChatOpenAI:
    """Lazy LLM client — avoids slow LangChain import during gunicorn worker boot."""
    return AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_api_endpoint or None,
        azure_deployment=settings.azure_openai_api_deployment_name or None,
        api_version=settings.azure_openai_api_version or None,
        api_key=settings.azure_openai_api_key or None,
        temperature=0,
        max_completion_tokens=4000,
        max_retries=3,
        timeout=120,
        streaming=False,
    )
 
 