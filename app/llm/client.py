# Provides the provider-neutral interface used by application services for LLM access.
# Routes requests to the configured provider without exposing provider-specific implementations.

from app.config import LLM_PROVIDER
from app.llm.openai.openai_client import create_chat_completion as create_openai_completion


def create_chat_completion(model, messages, temperature=None):
    if LLM_PROVIDER == "openai":
        return create_openai_completion(
            model=model,
            messages=messages,
            temperature=temperature,
        )

    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")